import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def test_retry():
    retry_strategy = Retry(
        total=3_000,
        backoff_factor=0.2,
        status_forcelist=[400, ],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    response = requests.get("https://httpbin.org/")
