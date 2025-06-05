from google.genai import types
from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .run_python_file import run_python_file
from .overwrite_file import overwrite_file

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = dict(function_call_part.args)
    # Always inject working_directory
    function_args["working_directory"] = "./calculator"

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    # Map function names to actual functions
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": overwrite_file,
    }

    func = function_map.get(function_name)
    if not func:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Actually call the function
    try:
        function_result = func(**function_args)
    except Exception as e:
        function_result = f"Exception during function call: {e}"

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )