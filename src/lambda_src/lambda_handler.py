import json
import logging
from src.lambda_src.utils import get_openai_model_response, validate_request_body

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    http_method = event.get("http_method", "POST")
    if http_method.upper() != "POST":
        logger.error(f"Invalid HTTP method used ({http_method})")
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "Invalid HTTP method used"
        }

    request_body = json.loads(event["body"])
    is_valid_request_body = validate_request_body(request_body)
    if not is_valid_request_body:
        logger.error(f"Invalid request body ({request_body})")
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "Invalid request body. Must be in form [{image_path:'', image_captions:''}, {...}, ...]"
        }

    # Call function get response from GPT-4
    initial_stories = get_openai_model_response(image_captions=request_body)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": initial_stories
    }
