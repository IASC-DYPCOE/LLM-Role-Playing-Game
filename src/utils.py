import re


def extract_json(input_text):
    """
    Extract JSON data from the input text.

    Args:
        input_text (str): The text to search for JSON data.

    Returns:
        list: A list of JSON data strings.
    """
    json_pattern = r"json\n(.*?)\n"

    matches = re.findall(json_pattern, input_text, re.DOTALL)

    return matches
