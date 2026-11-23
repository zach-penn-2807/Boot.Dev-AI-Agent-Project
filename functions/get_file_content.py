import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Retrieves the content (at most {MAX_CHARS} characters) of a specified file within the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        work_dir_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(work_dir_path, file_path))
        valid_target_file = os.path.commonpath([work_dir_path, target_file]) == work_dir_path

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        is_file = os.path.isfile(target_file)

        if not is_file:
            return f'Error: File not found or is not a regular file: "{file_path}"'

    
        with open(target_file, "r") as f:
            file_content = f.read(MAX_CHARS)
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content
    except Exception as e:
        return f"Error: {e}"
    
    