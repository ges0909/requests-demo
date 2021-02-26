import requests


def check_content(response, *args, **kwargs):
    response.status_code = 204  # No Content
    return response


def test_hooks():
    response = requests.get("https://httpbin.org/", hooks={"response": check_content})
    assert response.status_code == 204
