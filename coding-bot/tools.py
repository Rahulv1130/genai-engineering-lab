import subprocess
import os

def read_file(path: str):
    print(f"Calling Read File Function with path : {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return {
                "success": True,
                "content": f.read()
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def write_file(path: str, content: str):
    print(f"Calling write file with : {content}")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "success": True,
            "message": f"Successfully wrote to {path}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def list_files(path: str = "."):
    print("Calling list files")
    try:
        return {
            "success": True,
            "files": os.listdir(path)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def run_terminal_command(command: str):
    print(f"Calling Run Command : {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }

    except Exception as e:
        return {"error": str(e)}
    



tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the file to read."
                    }
                },
                "required": ["path"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file. Overwrites existing content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the file."
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write into the file."
                    }
                },
                "required": ["path", "content"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files and folders in a directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path.",
                        "default": "."
                    }
                }
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "run_terminal_command",
            "description": "Execute a terminal command and return the output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The terminal command to execute."
                    }
                },
                "required": ["command"]
            }
        }
    }
]