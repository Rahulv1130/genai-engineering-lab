# AI Terminal Agent

A simple AI-powered terminal assistant built with Python and the OpenAI API.

## Features

- Execute terminal commands
- Read files
- Write files
- List directory contents
- Multi-step tool calling loop
- Persistent conversation context during a session

## Tools

### `run_terminal_command(command)`
Executes terminal commands and returns:
- stdout
- stderr
- return code

### `read_file(path)`
Reads the contents of a file.

### `write_file(path, content)`
Creates or overwrites a file with the provided content.

### `list_files(path)`
Lists files and folders in a directory.

## Installation

```bash
pip install openai python-dotenv
```

## Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
```

## Run

```bash
python main.py
```

## Example Commands

```text
Create a file named index.java

Write a Java program to print the multiplication table of a number

Show me the contents of index.java

List all files in the current directory

Run javac index.java
```

## Project Structure

```text
.
├── main.py
├── tools.py
├── .env
└── README.md
```
