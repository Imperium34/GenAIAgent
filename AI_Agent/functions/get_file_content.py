import os
from google.genai import types


def get_file_content(working_directory, file_path):
    abs_work = os.path.abspath(working_directory)
    abs_target = abs_target = os.path.abspath(os.path.join(working_directory, file_path))
    if abs_work != abs_target and abs_target.startswith(abs_work + os.path.sep) == False:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(abs_target) == False:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    Max_chars = 10000

    with open(abs_target, "r") as f:
        file_content_string = f.read(Max_chars)
    
    return file_content_string


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="reads the contents of the specified file. Constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the file to read from, relative to the working directory.",
            ),
        },
    ),
)