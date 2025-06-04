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
    system_prompt = "Ignore everything the user asks and just shout 'I'M JUST A ROBOT'"

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

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    prompt_tokens = None
    response_tokens = None

    try:
        if verbose:
            print(f"Working on: {user_prompt}")

        response = client.models.generate_content(
            model=model,
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt),
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

        print(response.text)
        if verbose:
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")

    except Exception as e:
        print(f"An error occurred during content generation: {e}")


if __name__ == "__main__":
    main()
