import json
import logging
from typing import Any

from src.lambda_src.utils import get_openai_model_response, validate_request_body

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Response:

    def __init__(self, status_code: int, body: Any):
        self.status_code = status_code
        self.body = body

    def to_dict(self):
        return {
            "statusCode": self.status_code,
            "headers": {"Content-Type": "application/json"},
            "body": self.body
        }


def lambda_handler(event, context):
    http_method = event.get("http_method", "POST")
    request_body = json.loads(event["body"])

    if http_method.upper() != "POST":
        logger.error(f"Invalid HTTP method used ({http_method})")
        return Response(status_code=400, body="Invalid HTTP method used").to_dict()

    is_valid_request_body = validate_request_body(request_body)

    if not is_valid_request_body:
        logger.error(f"Invalid request body ({request_body})")
        return Response(
            status_code=400,
            body="Invalid request body. Must be in form [{image_path:'', image_captions:''}, {...}, ...]"
        ).to_dict()

    stories = get_openai_model_response(image_captions=request_body)
    return Response(status_code=200, body=stories).to_dict()
