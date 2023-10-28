from unittest.mock import patch

import pytest

from src.lambda_src.lambda_handler import get_openai_model_response, lambda_handler

FILEPATH = "src.lambda_src.lambda_handler"


@pytest.mark.parametrize(
    "event",
    [
        {
            "http_method": "POST"
        },
        {
            "http_method": "GET"
        },
        {
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


@patch(f"{FILEPATH}.requests.Response")
@patch(f"{FILEPATH}.requests")
def test_get_openai_response(mock_requests, mock_response, sample_openai_response):
    mock_response.json.return_value = sample_openai_response
    mock_requests.post.return_value = mock_response

    response = get_openai_model_response(image_captions=[])

    assert type(response) == list

    expected_keys = ["image_path", "image_caption", "story"]
    response_body_has_expected_keys = all(set(expected_keys) == set(item.keys()) for item in response)
    assert response_body_has_expected_keys

