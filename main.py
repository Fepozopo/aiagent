import os

from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        return

    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash-001"
    contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    prompt_tokens = None
    response_tokens = None

    try:
        response = client.models.generate_content(model=model, contents=contents)

        # Check if usage_metadata exists and is not None
        if response.usage_metadata:
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
        else:
            print("Warning: usage_metadata is None. Token count not available.")
            if response.prompt_feedback:
                print(f"Prompt Feedback: {response.prompt_feedback}")

        print(response.text)
        print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")

    except Exception as e:
        print(f"An error occurred during content generation: {e}")


if __name__ == "__main__":
    main()
