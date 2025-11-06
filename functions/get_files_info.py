import os
from pydantic import DirectoryPath
from google.genai import types

def get_files_info(working_directory, directory="."):
    abs_work = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, directory))
    if abs_work != abs_target and abs_target.startswith(abs_work + os.path.sep) == False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(abs_target) == False:
        return f'Error: "{directory}" is not a directory'

    if directory == ".":
        directory_path = "current"
    else:
        directory_path = directory

    final_string = f"Results for {directory_path} directory \n"
    for file in os.listdir(abs_target):
        final_string += f" - {file}: file_size={os.path.getsize(os.path.join(abs_target, file))} is_dir={os.path.isdir(os.path.join(abs_target, file))} \n"
    return final_string


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)