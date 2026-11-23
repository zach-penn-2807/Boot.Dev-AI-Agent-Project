import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file within the working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
     try:
        work_dir_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(work_dir_path, file_path))
        valid_target_file = os.path.commonpath([work_dir_path, target_file]) == work_dir_path
        is_file = os.path.isfile(target_file) 

        if not valid_target_file:
              return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not is_file:
              return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith('.py'):
              return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args != None:
              command.extend(args)

        completedprocess = subprocess.run(command, capture_output=True, timeout=30, text=True, cwd=work_dir_path )

        outputstr = []
     
        if completedprocess.returncode != 0:
              outputstr.append(f"Process exited with code {completedprocess.returncode}")

        if completedprocess.stdout == "" and completedprocess.stderr == "":
              outputstr.append(f"No output produced")

        if completedprocess.stdout:
              outputstr.append(f"STDOUT: {completedprocess.stdout}")

        if completedprocess.stderr:
              outputstr.append(f"STDERR: {completedprocess.stderr}")

        return "\n".join(outputstr)

     except Exception as e:
           return f"Error: executing Python file: {e}"