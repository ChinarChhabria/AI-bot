import os


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path,directory))
        valid_target_dir = os.path.commonpath([abs_path,target_dir])==abs_path
        if not valid_target_dir:
            return f'Result for \'{directory}\' directory:\nError: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir):
            return f'Result for \'{directory}\' directory:\nError: "{directory}" is not a directory'
        else:
            
            r_str = f"Result for {directory} directory\n"
            for i in os.listdir(target_dir):
                r_str+=f"- {i}: file_size={os.path.getsize(os.path.join(target_dir, i))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, i))}\n"
            
            return r_str      
    except Exception as e:
        return f"Error: {e}"
    
    
  