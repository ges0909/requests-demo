import requests


def test_random_user_generator():
    headers = {"X-Request-Id": "<my-request-id>"}  # custom headers 'X-...'
    response = requests.get(
        "https://randomuser.me/api/",
        headers=headers,
    )

    request = response.request
    assert request.url == "https://randomuser.me/api/"
    assert request.path_url == "/api/"
    assert request.method == "GET"
    assert request.headers == {
        "User-Agent": "python-requests/2.25.1",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "X-Request-Id": "<my-request-id>",
    }

    assert response.status_code == 200
    assert response.reason == "OK"
    # assert response.headers == {}
    assert response.headers.get("Content-Type") == "application/json; charset=utf-8"

    # content = response = response.text  # returns the response contents in unicode format
    # content = response = response.content  # returns the response contents in bytes
    dict_ = response = response.json()  # converts byte response in python dict

    pass


def test_read_bytes_and_save_as_local_file():
    response = requests.get("http://placegoat.com/200/200")
    if response.status_code == 200:
        if response.headers.get("Content-Type") == "image/jpeg":
            with open("goat.jpeg", "wb") as file:
                file.write(response.content)


def test_http_crud():
    requests.post("https://api.thedogapi.com/v1/breeds/1")
    requests.get("https://api.thedogapi.com/v1/breeds/1")
    requests.put("https://api.thedogapi.com/v1/breeds/1")
    requests.delete("https://api.thedogapi.com/v1/breeds/1")
