import re


def extract_json(input_text):
    json_pattern = r"(\{[\s\S]*\})"

    match = re.search(json_pattern, input_text)

    if match:
        json_content = match.group(1)
        return json_content
    else:
        print("No JSON content found")
