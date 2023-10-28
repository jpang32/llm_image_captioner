import json
import os
import requests

from typing import Any, Dict, List

OPEN_AI_TOKEN = os.getenv("OPEN_AI_TOKEN")
OPEN_AI_MODEL = os.getenv("OPEN_AI_MODEL")


def validate_request_body(body: Any):
    """Method for checking that the request body
    matches the expected structure.

    :param request body sent by the user
    :returns True if the request body is valid, else False
    """
    if type(body) != list:
        return False

    if not body:
        return False

    expected_keys = ["image_path", "image_caption"]
    if not all(set(expected_keys) == set(item.keys()) for item in body):
        return False

    return True


def get_openai_model_response(image_captions: List[Dict[str, str]]):
    """Makes call to OpenAI model using user input. First sets system content
    so model know the expected format for output.

    :param image_captions: List of dictionaries in format [{image_path:'', image_captions:''}, {...}, ...]
    :return: List of dictionaries in format [{image_path:'', image_captions:'', story:''}, {...}, ...]
    """

    url = "https://api.openai.com/v1/chat/completions"

    system_content = "Given a list of dictionaries of photo captions from a vlog in the format " \
                 " of this example: [{'image_path': 'birthday/BpsSOqpog98/" \
                 "BpsSOqpog98-0190.jpg', 'image_caption': 'a child blowing out candles" \
                 " at a birthday party'}, {...}, ...]" \
                 ", create a vivid story " \
                 "that incorporates the key elements from each " \
                 "photo. Turn the photo descriptions into a fun and " \
                 "engaging story. Your response should be a dictionary following the " \
                 "format of this example: [{'image_path': 'birthday/BpsSOqpog98/" \
                 "BpsSOqpog98-0190.jpg', 'image_caption': 'a child blowing out candles" \
                 " at a birthday party', 'story': 'the story you generated'}, {...}, ...]"

    user_content = json.dumps(image_captions)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPEN_AI_TOKEN}"
    }

    body = {
        "model": OPEN_AI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_content
            },
            {
                "role": "user",
                "content": user_content
            }
        ]
    }

    open_ai_response = requests.post(
        url=url,
        json=body,
        headers=headers
    ).json()

    model_content = open_ai_response["choices"][0]["message"]["content"]

    return json.loads(model_content)
