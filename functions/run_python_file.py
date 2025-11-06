import os
import subprocess
import sys
from google.genai import types
from pydantic_core.core_schema import none_schema

def run_python_file(working_directory, file_path, args=[]):   
    abs_work = os.path.abspath(working_directory)
    abs_target = abs_target = os.path.abspath(os.path.join(working_directory, file_path))
    
    if abs_work != abs_target and abs_target.startswith(abs_work + os.path.sep) == False:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if os.path.exists(abs_target) == False:
        return f'Error: File "{file_path}" not found.'
    if file_path.endswith(".py") == False:
        return f'Error: "{file_path}" is not a Python file.'

    result = subprocess.run(
        [sys.executable, abs_target, *args],
        capture_output=True,
        text=True,
        timeout=30
    )

    final_output = ""

    if result.returncode != 0:
        final_output += f"Process exited with code {result.returncode}\n"
    if result.stdout == "":
        final_output += "STDOUT: No output produced.\n"
    else:
        final_output += f"STDOUT: {result.stdout}\n"
    if  result.stderr:
        final_output += f"STDERR: {result.stderr}\n"
    return final_output


schema_run_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs the specified python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to the python file that will be run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="the optional arguments that will be given to the python file"
            ),
        },
    ),
)
