# aiagent

## Overview

**aiagent** is a command-line AI coding agent powered by Google Gemini, designed to help you interact with your codebase and perform file operations using natural language prompts. It can list files, read file contents, execute Python scripts, and write or overwrite files, all within a secure working directory.

The project also includes a sample calculator app to demonstrate file operations and function execution.

---

## Features

- **Natural Language Interface:** Send prompts to Gemini AI to perform coding and file operations.
- **File Management:** List, read, and write files securely within a working directory.
- **Python Execution:** Run Python scripts and capture their output.
- **Extensible Functions:** Easily add new operations by extending the `functions/` module.
- **Sample Calculator App:** Includes a simple calculator with a pretty text-based renderer.

---

## Getting Started

### Prerequisites

- Python 3.8+
- [Google Gemini API Key](https://ai.google.dev/)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Fepozopo/aiagent.git
   cd aiagent
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Gemini API key in a `.env` file:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

---

## Usage

### Run the AI Agent

```bash
python main.py "<your prompt here>"
```

Example:
```bash
python main.py "List all files in the calculator directory."
```

### Run the Calculator App

```bash
python calculator/main.py "3 + 5 * 2"
```

---

## Project Structure

- `main.py` — Entry point for the AI agent CLI
- `functions/` — Modular functions for file and code operations
- `calculator/` — Sample calculator app and its modules
- `requirements.txt` — Python dependencies

---

## Testing

Run the provided tests:

```bash
python tests.py
python calculator/tests.py
```

---

## License

This project is licensed under the MIT License.