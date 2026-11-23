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
     work_dir_path = os.path.abspath(working_directory)
     target_dir = os.path.normpath(os.path.join(work_dir_path, directory))
     valid_target_dir = os.path.commonpath([work_dir_path, target_dir]) == work_dir_path

     if valid_target_dir != True:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

     valid_dir = os.path.isdir(target_dir)

     if not valid_dir:
        return f'Error: "{directory}" is not a directory'

     if valid_dir:
        dir_content = os.listdir(target_dir)
        file_info = []
        for file in dir_content:
           name = file
           size = os.path.getsize(os.path.join(target_dir, file))
           is_dir = os.path.isdir(os.path.join(target_dir, file))
           file_str = f"- {name}: file_size={size} bytes, is_dir={is_dir}"
           file_info.append(file_str)
        return "\n".join(file_info)
        
        
   
   except Exception as e:
       return f"Error: {e}"
       