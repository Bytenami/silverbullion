import json
import mock
import requests
from silverbullion import main


class mock_request:
    def __init__(self, *args, **kwargs):
        with open("tests/test_files/gold_page.html", "r") as fp:
            data = fp.read()
        self.text = data


@mock.patch("requests.get", mock_request)
def test_main():
    response = main.lambda_handler("", "")
    expected = {
        'statusCode': 200,
        'body': 125438
    }
    assert response == expected