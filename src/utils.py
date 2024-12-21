import json
import re


def extract_json(input_text):
    """
    Extracts and formats JSON from input text, handling common issues like emojis
    and markdown code blocks.

    Args:
        input_text (str): Input text containing JSON

    Returns:
        str: Properly formatted JSON string
    """
    # Remove leading/trailing whitespace
    input_text = input_text.strip()

    # Remove markdown code block syntax if present
    input_text = re.sub(r"```(?:json)?\n?", "", input_text)

    # Handle potential trailing backticks
    input_text = input_text.strip("`")

    try:
        # First try to parse as is
        json_object = json.loads(input_text)
    except json.JSONDecodeError:
        # If that fails, try cleaning the string further
        # Remove newlines and extra whitespace
        input_text = " ".join(input_text.split())

        try:
            json_object = json.loads(input_text)
        except json.JSONDecodeError as e:
            raise Exception(f"Could not parse JSON: {str(e)}")

    return json.dumps(json_object, ensure_ascii=False, indent=2)
