from unittest.mock import patch

from src.lambda_src.lambda_handler import get_openai_model_response, lambda_handler

FILEPATH = "src.lambda_src.lambda_handler"


@patch(f"{FILEPATH}.requests.Response")
@patch(f"{FILEPATH}.requests")
def test_get_openai_response(mock_requests, mock_response, sample_openai_response):
    mock_response.json.return_value = sample_openai_response
    mock_requests.post.return_value = mock_response

    response = get_openai_model_response(image_captions=[])
    response_body = response["body"]

    assert type(response) == dict
    assert response["headers"] == {
            "Content-Type": "application/json"
        }
    assert response["statusCode"] == 200
    assert type(response_body) == list

    expected_keys = ["image_path", "image_caption", "story"]
    response_body_has_expected_keys = all(set(expected_keys) == set(item.keys()) for item in response_body)
    assert response_body_has_expected_keys

