import json
import requests
import socket
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
    pattern = r"Turns remaining: (\d+)/5"

    match = re.search(pattern, text)
    if match:
        turns = match.group(1)

    return int(turns)


def get_windows_host():
    with open("/etc/resolv.conf") as f:
        for line in f:
            if "nameserver" in line:
                return line.split()[1]
    return None


def send_prompt_to_llama(prompt, model="llama3.2:3b", temperature=0.7):
    prompt += "\nGenerate an ascii art of the above text and nothing else."
    windows_host = get_windows_host()
    url = f"http://{windows_host}:11434/api/generate"

    data = {"model": model, "prompt": prompt, "temperature": temperature}

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()

        full_response = ""
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                if "response" in json_response:
                    full_response += json_response["response"]

        return full_response

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"
