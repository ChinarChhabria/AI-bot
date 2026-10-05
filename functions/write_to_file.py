import os

schema_write_to_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "writes to a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "file path to access the file and write content",
                },
                "content":{
                    "type":"string",
                    "description":"The content to write to the file."
                }
            },
            "required":["file_path","content"]
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs,file_path))
        valid_path = os.path.commonpath([working_directory_abs,target_file])==working_directory_abs
        if not valid_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        else:
            os.makedirs(os.path.dirname(target_file),exist_ok=True)

            with open(target_file,'w') as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
    