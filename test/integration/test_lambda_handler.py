import json
import pytest
from src.lambda_src.lambda_handler import lambda_handler


@pytest.mark.parametrize(
    "event",
    [
        {
            "httpMethod": "POST",
            "body": """[
                {
                    "image_path": "test_path/image1.png",
                    "image_caption": "a child pulls on a tablecloth"
                },
                {
                    "image_path": "other_test_path/image2.png",
                    "image_caption": "a child starts to pull a tablecloth off of the table"
                },
                {
                    "image_path": "other_other_test_path/image2.png",
                    "image_caption": "a child covered in food in front of a table with food on the floor"
                }
            ]""",
        }
    ],
)
def test_lambda_handler(event):
    response = lambda_handler(event=event, context=None)

    assert response["statusCode"] == 200
    assert response["headers"] == {"Content-Type": "application/json"}

    response_body = response["body"]
    for i, image_caption in enumerate(json.loads(event["body"])):
        assert response_body[i]["image_path"] == image_caption["image_path"]
        assert response_body[i]["image_caption"] == image_caption["image_caption"]
        assert "story" in response_body[i]
