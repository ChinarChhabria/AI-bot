import os
from pathlib import Path
import sys


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_files_content",
        "description": "gets the content inside of files",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path to get content",
                },
            },
        },
    },
}


# Get the path of the parent directory
parent_dir = Path(__file__).resolve().parent.parent

# Add the parent directory to sys.path
sys.path.append(str(parent_dir))

# Now you can import your module directly
from config import CHARACTER_LIMIT

def get_file_content(working_directory:str,file_path:str)->str:
    try:
        
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs,file_path))
        valid_path = os.path.commonpath([working_directory_abs,target_file])==working_directory_abs
        if not valid_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(target_file) as f:
            content = f.read(CHARACTER_LIMIT)

            print(content[:10])
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {CHARACTER_LIMIT} characters]'
            return content
    except Exception as e:
        return f"Error: {e}"

