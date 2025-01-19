# Code Improvement Assistant using Mistral AI

## Overview

The Code Improvement Assistant is a command-line interface (CLI) tool designed to enhance a program code using the Mistral Codestral LLM. This tool leverages the power of Mistral AI to automatically improve your code based on specified criteria indicated in a well prepared prompt.

## Features

- **Automatic Code Improvement**: Uses Mistral AI to suggest improvements to your code.
- **Custom Prompts**: Allows you to specify custom prompts for code improvement.
- **Rich Output**: Utilizes the `rich` library for enhanced console output.
- **Progress Tracking**: Displays progress during the code improvement process.

## Requirements

- Python 3.13 or higher
- Mistral AI API key
- `mistralai` and `rich` Python packages

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/code-improvement-assistant.git
    cd code-improvement-assistant
    ```

2. **Install dependencies**:
    ```sh
    pip install mistralai rich
    ```

3. **Set up the Mistral API key**:
    ```sh
    export MISTRAL_API_KEY='your_mistral_api_key_here'
    ```

## Usage

### Basic Usage

To improve a Python code file, use the following command:
```sh
python program.py -i input_code.py -o improved_code.py
```

### With Custom Prompt

To specify a custom prompt for code improvement:
```sh
python program.py -i input_code.py -o improved_code.py -p "Add type hints and docstrings"
```

### Show Help

To display the help message:
```sh
python program.py --help
```

### Show Version

To display the program version:
```sh
python program.py --version
```

## Examples

### Basic Example

```sh
python program.py -i input_code.py -o improved_code.py
```

### Custom Prompt Example

```sh
python program.py -i input_code.py -o improved_code.py -p "Add type hints and docstrings"
```

### Help Example

```sh
python program.py --help
```

## Environment Variables

- `MISTRAL_API_KEY`: Your Mistral AI API key.

## Commands

- `-h, --help`: Show this help message.
- `-o, --output`: Specify output file path for improved code.
- `-i, --input`: Specify input code file path.
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
