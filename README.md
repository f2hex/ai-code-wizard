# Console Based Code Generation Assistant

## Overview

This project is about a LLM code generation assistant using a simple command-line interface (CLI) tool designed to create new
program or to enhance an existing one code using a Gen AI based backend API using specified criteria indicated in a well prepared
prompt.  Currently Ollama and Mistral are implemented.

## Features

- **Automatic Code Improvement**: Uses Mistral AI to suggest improvements to your code.
- **Custom Prompts**: Allows you to specify custom prompts for code improvement.
- **Rich Output**: Utilizes the `rich` library for enhanced console output.
- **Progress Tracking**: Displays progress during the code improvement process.

## Requirements

- Python 3.13 or higher
-  Depending on the backend: API key (Mistral)
- `ollama`, `mistralai` and `rich` Python packages

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/f2hex/ai-code-wizard
    cd ai-code-wizard
    ```

2. **Install dependencies**:
    ```sh
    pip install ollama mistralai rich
    ```
3. Install `uv` if not available already:
    ```sh
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    if you prefer to install it through a package manager just look the [software main site](https://docs.astral.sh/uv/) on how to
    do that.

4. **Set up the Mistral API key** (if needed):
    ```sh
    export MISTRAL_API_KEY='your_mistral_api_key_here'
    ```
5. For an easy way to use it just make the main program executable:
    ```sh
    chmod +x ./codewizard.py
    ```


## Usage

### Basic Usage

To improve a Python code file, use the following command:
```sh
./codewizard.py -i input_code.py -o improved_code.py
```

an easy way to use is to copy the program in a directory included in the `PATH` env. var and also create an alias for it like this:

```sh
alias cw=codewizard.py
```

### With Custom Prompt

To specify a custom prompt for code improvement:
```sh
cw -i input_code.py -o improved_code.py -p "Add type hints and docstrings"
```

### Show Help

To display the help message:
```sh
cw --help
```

### Show Version

To display the program version:
```sh
cw --version
```

## Examples

### Basic Example

```sh
cw -i input_code.py -o improved_code.py
```

### Custom Prompt Example

```sh
cw -i input_code.py -o improved_code.py -p "Add type hints and docstrings"
```

### Help Example

```sh
cw --help
```

## Environment Variables

- `MISTRAL_API_KEY`: Your Mistral AI API key.

## Commands

- `-h, --help`: Show this help message.
- `-o, --output`: Specify output file path for improved code.
- `-i, --input`: Specify input code file path (optional). Not required if you create code from scratch.
- `-p, --prompt`: Custom prompt for code improvement (optional).
- `--version`: Show program version.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Author

Franco Fiorese <fcoder@f2hex.net>

## Date

January 2025
