import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_function import call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        sys.exit("Error: GEMINI_API_KEY not found in environment variables.")

    client = genai.Client(api_key=api_key)
    model = "gemini-2.0-flash-001"

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

    If you write or overwrite any files, list each of those files, stating whether you created them or modified them.
    """

    parser = argparse.ArgumentParser(description="Gemini AI Command Line Client")
    parser.add_argument("prompt", nargs="+", help="Prompt to send to Gemini AI")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    user_prompt = " ".join(args.prompt)
    if not user_prompt:
        sys.exit(
            "Error: No prompt provided. Please provide a prompt to send to Gemini AI."
        )

    verbose = args.verbose
    prompt_tokens = None
    response_tokens = None

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

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
    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Retrieves the content of a file in the specified directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to retrieve, relative to the working directory.",
                ),
            },
        ),
    )
    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Runs a Python file in the specified directory and returns the output.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the Python file to run, relative to the working directory.",
                ),
            },
        ),
    )
    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes content to a file in the specified directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to write, relative to the working directory.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file.",
                ),
            },
        ),
    )
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    try:
        if verbose:
            print(f"Working on: {user_prompt}")

        max_iterations = 20
        for iteration in range(max_iterations):
            response = client.models.generate_content(
                model=model,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            # Track tokens if available
            if response.usage_metadata:
                prompt_tokens = response.usage_metadata.prompt_token_count
                response_tokens = response.usage_metadata.candidates_token_count
            else:
                if verbose:
                    print("Warning: usage_metadata is None. Token count not available.")
                if response.prompt_feedback:
                    print(f"Prompt Feedback: {response.prompt_feedback}")

            function_called = False
            # Add all candidates' .content to messages
            if hasattr(response, "candidates") and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, "content"):
                        messages.append(candidate.content)
                        # Check for function call in parts
                        if hasattr(candidate.content, "parts"):
                            for part in candidate.content.parts:
                                if (
                                    hasattr(part, "function_call")
                                    and part.function_call
                                ):
                                    function_called = True
                                    function_call = part.function_call
                                    function_call_result = call_function(
                                        function_call, verbose=verbose
                                    )
                                    # Append returned types.Content to messages
                                    messages.append(function_call_result)
                                    # Optionally print function response if verbose
                                    if verbose:
                                        try:
                                            response_obj = function_call_result.parts[
                                                0
                                            ].function_response.response
                                            print(f"-> {response_obj}")
                                        except Exception:
                                            print(
                                                "Function call did not return a valid response object."
                                            )
            # If a function was called, continue to next iteration
            if function_called:
                continue
            # Otherwise, print the LLM's final response and break
            else:
                # Fallback: print text if available
                if hasattr(response, "text") and response.text:
                    print(response.text)
                else:
                    # Try to print any text parts from candidates
                    for candidate in getattr(response, "candidates", []):
                        if hasattr(candidate, "content") and hasattr(
                            candidate.content, "parts"
                        ):
                            for part in candidate.content.parts:
                                if hasattr(part, "text") and part.text:
                                    print(part.text)
                break

        if verbose:
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")

    except Exception as e:
        print(f"An error occurred during content generation: {e}")


if __name__ == "__main__":
    main()
