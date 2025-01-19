#!/usr/bin/env -S uv -q run
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "mistralai",
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
    -h, --help         Show this help message
    -o, --output       Specify output file path for improved code
    -i, --input        Specify input code file path
    -p, --prompt       Custom prompt for code improvement (optional)
    --version         Show program version

Examples:
    # Basic usage
    python program.py -i input_code.py -o improved_code.py

    # With custom prompt
    python program.py -i input_code.py -o improved_code.py -p "Add type hints and docstrings"

    # Show help
    python program.py --help
"""

import os
import sys
import argparse
from mistralai import Mistral
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.progress import Progress

class CodeImprovementAssistant:
    def __init__(self):
        self.console = Console()
        self.args = self.parse_arguments()
        self.api_key = os.environ.get("MISTRAL_API_KEY")
        self.client = self.initialize_mistral_client()

    def show_help(self):
        """
        Display the help message and exit.
        """
        help_text = """
        Code Improvement Assistant using Mistral AI

        Environment Variables Required:
            MISTRAL_API_KEY    Your Mistral AI API key

        Commands:
            -h, --help         Show this help message
            -o, --output       Specify output file path for improved code
            -i, --input        Specify input code file path
            -p, --prompt       Custom prompt for code improvement (optional)
            --version         Show program version

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
            help="Output file path for the generated code"
        )
        required.add_argument(
            "-i", "--input",
            required=True,
            help="Input program code file path"
        )

        optional.add_argument(
            "-p", "--prompt",
            default="Look at the code included below and make improvements in terms of better maintenance and readability",
            help="Custom prompt for code improvement"
        )

        return parser.parse_args()

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

    def read_code_file(self, file_path: str) -> str:
        """
        Read the input code file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as finp:
                code = finp.read()
                self.console.print("\n[bold green]Input Code:[/bold green]")
                self.console.print(Panel(Syntax(code, "python", theme="monokai")))
                return code
        except FileNotFoundError:
            self.console.print(f"[bold red]Error:[/bold red] Input file '{file_path}' not found", style="red")
            sys.exit(1)
        except Exception as e:
            self.console.print(f"[bold red]Error:[/bold red] Failed to read input file: {str(e)}", style="red")
            sys.exit(1)

    def write_output_file(self, file_path: str, content: str):
        """
        Write the improved code to the output file.
        """
        try:
            with open(file_path, "w", encoding='utf-8') as fout:
                fout.write(content)
                fout.write("\n")
            self.console.print(f"\n[bold green]Successfully wrote improved code to:[/bold green] {file_path}")
        except Exception as e:
            self.console.print(f"[bold red]Error:[/bold red] Failed to write output file: {str(e)}", style="red")
            sys.exit(1)

    def generate_improved_code(self) -> str:
        """
        Generate improved code using Mistral AI.
        """
        code = self.read_code_file(self.args.input)
        message = [
            {
                "role": "user",
                "content": f"{self.args.prompt}\n```python\n{code}\n```"
            }
        ]

        self.console.print("\n[bold blue]Generating improved code...[/bold blue]")
        with Progress() as progress:
            task = progress.add_task("[cyan]Processing...", total=None)
            try:
                chat_response = self.client.chat.complete(
                    model="codestral-latest",
                    messages=message
                )
            except Exception as e:
                self.console.print(f"[bold red]Error:[/bold red] API call failed: {str(e)}", style="red")
                sys.exit(1)
            progress.update(task, completed=100)

        improved_code = chat_response.choices[0].message.content
        self.console.print("\n[bold green]Generated Code:[/bold green]")
        self.console.print(Panel(Syntax(improved_code, "python", theme="monokai")))
        return improved_code

    def run(self):
        """
        Main method to run the code improvement process.
        """
        improved_code = self.generate_improved_code()
        self.write_output_file(self.args.output, improved_code)

if __name__ == "__main__":
    assistant = CodeImprovementAssistant()
    assistant.run()
