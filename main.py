import argparse
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


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

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
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

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    try:
        if verbose:
            print(f"Working on: {user_prompt}")

        response = client.models.generate_content(
            model=model,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        # Check if usage_metadata exists and is not None
        if response.usage_metadata:
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
        else:
            if verbose:
                print("Warning: usage_metadata is None. Token count not available.")
            if response.prompt_feedback:
                print(f"Prompt Feedback: {response.prompt_feedback}")


        # Check if the LLM called a function
        if hasattr(response, "candidates") and response.candidates:
            for candidate in response.candidates:
                if hasattr(candidate, "content") and hasattr(candidate.content, "parts"):
                    for part in candidate.content.parts:
                        if hasattr(part, "function_call") and part.function_call:
                            function_call = part.function_call
                            print(f"Calling function: {function_call.name} with arguments: {function_call.args}")
                        elif hasattr(part, "text") and part.text:
                            print(part.text)
        else:
            # Fallback: print text if available
            if hasattr(response, "text"):
                print(response.text)

        if verbose:
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")

    except Exception as e:
        print(f"An error occurred during content generation: {e}")


if __name__ == "__main__":
    main()
