#!/usr/bin/env -S uv -q run
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "mistralai",
#     "ollama",
#     "rich",
# ]
# ///

"""
Code Improvement Assistant using Mistral AI

Author: Franco Fiorese <fcoder@f2hex.net>
Date: Jan 2025

Environment Variables Required:
    MISTRAL_API_KEY    Your Mistral AI API key

Commands:
    -h, --help      Show this help message
    -o, --output    Specify output file path for improved code
    -i, --input:    Specify input code file path (optional). Not required if you create code from scratch.
    -p, --prompt    Custom prompt for code improvement (optional)
    --version       Show program version

Examples:
    # Basic usage
    ./codewizard.py -i input_code.py -o improved_code.py

    # With custom prompt
    .codewizard.py -i input_code.py -o improved_code.py -p "Add type hints and docstrings"

    # Show help
    codewizard.py --help
"""

import os
import sys
import argparse
import json
from mistralai import Mistral
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.progress import Progress

DEFAULT_PROMPT = """
Look at the code included below and make improvements in terms of better maintenance and readability
"""

COMPLEMENT_PROMPT = """
write any generated code, in python language, within an opening <code> tag and the closing one </code>, create also a structured
documentation about the generated code, how it works and it is organized and put all that related content enclosed between a single
pair of leading <doc> and trailing </doc> tags. All those tags must be start at the beginning of a line. Do not enclose the
generated code in backtics (```).
"""

SYSTEM_PROMPT = """
You are an expert Python developer with extensive experience in software development, data analysis, and web application
design. Your role is to assist users by providing accurate and practical advice on Python programming, including syntax, libraries,
and best practices. Offer clear code examples and explanations for various concepts, help debug and optimize code, and share
insights on software development methodologies. Communicate in a clear and concise manner, using appropriate technical terminology
while ensuring that complex ideas are easily understood. Stay updated on the latest trends in the Python ecosystem and encourage
best practices in coding and software development.
"""

class CodeAssistant:
    def __init__(self, console: Console, input_code_file: str, out_filename: str, prompt: str):
        self.console = console
        self.api_key = os.environ.get("MISTRAL_API_KEY")
        self.client = self.initialize_mistral_client()
        self.prompt = prompt
        self.input_code_file = input_code_file
        self.out_filename = out_filename

    def initialize_mistral_client(self) -> Mistral:
        """
        Initialize the Mistral client.
        """
        if not self.api_key:
            self.console.print("[bold red]Error:[/bold red] MISTRAL_API_KEY environment variable is not set", style="red")
            sys.exit(1)

        try:
            return Mistral(api_key=self.api_key)
        except Exception as e:
            self.console.print(f"[bold red]Error:[/bold red] Failed to initialize Mistral client: {str(e)}", style="red")
            sys.exit(1)

    def read_code_file(self) -> str:
        """
        Read the input code file.
        """
        try:
            with open(self.input_code_file, 'r', encoding='utf-8') as finp:
                code = finp.read()
                self.console.print("\n[bold green]Input Code:[/bold green]")
                self.console.print(Panel(Syntax(code, "python", theme="monokai")))
                return code
        except FileNotFoundError:
            self.console.print(f"[bold red]Error:[/bold red] Input file '{self.input_code_file}' not found", style="red")
            sys.exit(1)
        except Exception as e:
            self.console.print(f"[bold red]Error:[/bold red] Failed to read input file: {str(e)}", style="red")
            sys.exit(1)

    def dump_api_request(self, request):
        with open("api_request.json", 'w', encoding='utf-8') as fout:
            json.dump(request, fout, indent=4)

    def generate_code_and_doc(self) -> str:
        """
        Generate code or improved code using Mistral AI.
        """
        if self.input_code_file is not None:
            code = f"\n```python\n{self.read_code_file()}\n```\n"
        else:
            code = ""
        prompt = f"{self.prompt}; {COMPLEMENT_PROMPT}"
        messages = [
            { "role": "system", "content": SYSTEM_PROMPT },
            { "role": "user", "content": f"{prompt}{code}" }
        ]
        self.console.print("\n[bold blue]Generating improved code...[/bold blue]")
        with Progress() as progress:
            task = progress.add_task("[cyan]Processing...", total=None)
            try:
                chat_response = self.client.chat.complete(
                    model="codestral-latest",
                    messages=messages
                )
            except Exception as e:
                self.console.print(f"[bold red]Error:[/bold red] API call failed: {str(e)}", style="red")
                sys.exit(1)
            progress.update(task, completed=100)

        self.dump_api_request(messages)
        improved_code = chat_response.choices[0].message.content
        self.console.print("\n[bold green]Generated Code:[/bold green]")
        self.console.print(Panel(Syntax(improved_code, "python", theme="monokai")))
        return improved_code

    def write_output_files(self, content: str):
        """
        Write the improved code and documentation to the output files.
        """
        code = []
        doc = []
        in_code_block = False
        in_doc_block = False

        for line in content.splitlines():
            if line.strip() == "<code>":
                in_code_block = True
                continue
            elif line.strip() == "</code>":
                in_code_block = False
                continue
            elif line.strip() == "<doc>":
                in_doc_block = True
                continue
            elif line.strip() == "</doc>":
                in_doc_block = False
                continue

            if in_code_block:
                code.append(line)
            elif in_doc_block:
                doc.append(line)

        code_content = "\n".join(code)
        doc_content = "\n".join(doc)

        try:
            code_file = f"{self.out_filename}.py"
            with open(code_file, "w", encoding='utf-8') as fout:
                fout.write(code_content)
                fout.write("\n")
            self.console.print(f"\n[bold green]Successfully wrote improved code to:[/bold green] {code_file}")

            doc_file = f"{self.out_filename}.md"
            with open(doc_file, "w", encoding='utf-8') as fout:
                fout.write(doc_content)
                fout.write("\n")
            self.console.print(f"\n[bold green]Successfully wrote documentation to:[/bold green] {doc_file}")
        except Exception as e:
            self.console.print(f"[bold red]Error:[/bold red] Failed to write output files: {str(e)}", style="red")
            sys.exit(1)

    def run(self):
        """
        Main method to run the code improvement process.
        """
        code_and_doc = self.generate_code_and_doc()
        self.write_output_files(code_and_doc)

class ArgParser():
    def __init__(self, console):
        self.console = console

    def show_help(self):
        """
        Display the help message and exit.
        """
        help_text = """
        Console Based Code Generation Assistant

        Environment Variables Required (if using the related service):
            MISTRAL_API_KEY    Your Mistral AI API key

        Commands:
            -h, --help     Show this help message
            -o, --output   Specify output file path for improved code
            -i, --input    Specify input code file path
            -i, --input:   Specify input code file path (optional). Not required if you create code from scratch.
            -p, --prompt   Custom prompt for code improvement (optional)
            --version      Show program version

        Examples:
            # Basic usage
            python program.py -i input_code.py -o improved_code.py

            # With custom prompt
            python program.py -i input_code.py -o improved_code.py -p "Add type hints and docstrings"

            # Show help
            python program.py --help
        """
        self.console.print(Panel(help_text, title="Help", border_style="blue"))
        sys.exit(0)

    def parse_arguments(self) -> argparse.Namespace:
        """
        Parse command-line arguments.
        """
        if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
            self.show_help()

        parser = argparse.ArgumentParser(
            description="Code improvement assistant using Mistral AI",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            add_help=False  # Disable default help
        )

        required = parser.add_argument_group('required arguments')
        optional = parser.add_argument_group('optional arguments')

        optional.add_argument(
            '-h', '--help',
            action='store_true',
            help='Show this help message'
        )
        optional.add_argument(
            '--version',
            action='version',
            version='%(prog)s 1.0.0',
            help='Show program version'
        )
        required.add_argument(
            "-o", "--output",
            required=True,
            dest='out_filename',
            help="Output file path for the generated code"
        )
        optional.add_argument(
            "-i", "--input",
            dest='input_code_file',
            help="Input program code file path (if any)"
        )
        required.add_argument(
            "-p", "--prompt",
            dest='prompt',
            default=DEFAULT_PROMPT,
            help="Custom prompt for code improvement"
        )
        return parser.parse_args()

def main():
    console = Console()
    ap = ArgParser(console)
    args= ap.parse_arguments()
    assistant = CodeAssistant(console,input_code_file=args.input_code_file, out_filename=args.out_filename, prompt=args.prompt)
    assistant.run()

if __name__ == "__main__":
    main()
