import requests


def check_content(response, *args, **kwargs):
    response.status_code = 204  # No Content
    return response


def test_hooks():
    response = requests.get("https://httpbin.org/", hooks={"response": check_content})
    assert response.status_code == 204


def test_session():
    session = requests.Session()
    session.hooks['response'] = [check_content, ]
    assert session.get("https://httpbin.org/").status_code == 204
