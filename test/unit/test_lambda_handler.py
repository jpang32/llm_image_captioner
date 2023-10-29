from unittest.mock import patch
import pytest

from src.lambda_src.lambda_handler import lambda_handler

FILEPATH = "src.lambda_src.lambda_handler"


@pytest.mark.parametrize(
    "event",
    [
        {
            "body": '[{"image_path": "blah", "image_caption": "blah"}]',
            "http_method": "POST"
        },
        {
            "body": '[{"image_path": "blah", "image_caption": "blah"}]',
            "http_method": "GET"
        },
        {
            "body": '[{"image_path": "blah", "image_caption": "blah"}]',
            "http_method": "PUT"
        }
    ]
)
@patch(f"{FILEPATH}.get_openai_model_response")
def test_lambda_handler(mock_openai_model_response, event, sample_openai_response):
    mock_openai_model_response.return_value = sample_openai_response
    response = lambda_handler(event=event, context=None)

    assert type(response) == dict
    assert response["headers"] == {
        "Content-Type": "application/json"
    }
    assert "body" in response

    if event["http_method"] != "POST":
        mock_openai_model_response.assert_not_called()
        assert 400 <= response["statusCode"] <= 499
    else:
        mock_openai_model_response.assert_called_once()
        assert 200 <= response["statusCode"] <= 299
