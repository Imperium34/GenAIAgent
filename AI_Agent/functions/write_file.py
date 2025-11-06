import os
from google.genai import types


def write_file(working_directory, file_path, content):
    abs_work = os.path.abspath(working_directory)
    abs_target = abs_target = os.path.abspath(os.path.join(working_directory, file_path))
    if abs_work != abs_target and abs_target.startswith(abs_work + os.path.sep) == False:
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
    if os.path.exists(os.path.dirname(abs_target)) == False:
        os.makedirs(os.path.dirname(abs_target))
    with open(abs_target, "w") as f:
        f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes or overwrites wanted content to a file. Constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the file to write the content in, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content that will be written to the file"
            ),
        },
    ),
)