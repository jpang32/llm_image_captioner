import json
import pytest
from src.lambda_src.lambda_handler import get_openai_model_response


@pytest.mark.parametrize(
    "image_captions",
    [
        [
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
        ]
    ]
)
def test_get_openai_model_response(image_captions):

    result = get_openai_model_response(image_captions)
    result_body = result["body"]

    for i, image_caption in enumerate(image_captions):
        assert result_body[i]["image_path"] == image_caption["image_path"]
        assert result_body[i]["image_caption"] == image_caption["image_caption"]
        assert "story" in result_body[i]

