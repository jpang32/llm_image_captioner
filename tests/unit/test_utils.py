import pytest
from unittest.mock import patch

from lambdas.inference.utils import get_openai_model_response, validate_request_body

FILEPATH = "lambdas.inference.utils"


@pytest.mark.parametrize(
    ("request_body", "expected"),
    [
        ([], False),
        ([{"image_path": "blah"}], False),
        ([{"image_path": "blah", "image_caption": "blah"}], True),
    ],
)
def test_validate_request_body(request_body, expected):
    assert validate_request_body(request_body) == expected


@patch(f"{FILEPATH}.requests.Response")
@patch(f"{FILEPATH}.requests")
def test_get_openai_response(mock_requests, mock_response, sample_openai_response):
    mock_response.json.return_value = sample_openai_response
    mock_requests.post.return_value = mock_response
    test = mock_requests.post.return_value.json.return_value

    response = get_openai_model_response(image_captions=[])

    assert type(response) == list

    expected_keys = ["image_path", "image_caption", "story"]
    response_body_has_expected_keys = all(
        set(expected_keys) == set(item.keys()) for item in response
    )

    assert response_body_has_expected_keys
