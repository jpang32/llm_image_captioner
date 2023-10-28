import logging
import json
import os
import requests

from typing import Dict, List

logger = logging.getLogger()
logger.setLevel(logging.INFO)

OPEN_AI_TOKEN = os.getenv("OPEN_AI_TOKEN")
OPEN_AI_MODEL = os.getenv("OPEN_AI_MODEL")


def lambda_handler(event, context):
    # get header method and check if POST
    # If not, return error
    http_method = event.get("http_method", "POST")
    if http_method.upper() != "POST":
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "isBase64Encoded": False,
            "body": json.dumps({"message":"Invalid HTTP method used"})
        }

    # Call function get response from GPT-4
    initial_stories = get_openai_model_response()

    return {"message": initial_stories}


def get_openai_model_response(image_captions: List[Dict[str, str]]):

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

    response_body = json.loads(model_content)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": response_body
    }


