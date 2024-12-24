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
    input_text = input_text.strip()

    input_text = re.sub(r"```(?:json)?\n?", "", input_text)

    input_text = input_text.strip("`")

    try:
        json_object = json.loads(input_text)
    except json.JSONDecodeError:
        input_text = " ".join(input_text.split())

        try:
            json_object = json.loads(input_text)
        except json.JSONDecodeError as e:
            raise Exception(f"Could not parse JSON: {str(e)}")

    return json.dumps(json_object, ensure_ascii=False, indent=2)


def extract_lives_remaining(text: str) -> int:
    pattern = r"Turns remaining: (\d+)/10"

    match = re.search(pattern, text)
    if match:
        turns = match.group(1)

    return int(turns)
