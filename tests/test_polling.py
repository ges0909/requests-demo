import logging

import polling
import pytest
import requests
import queue

log = logging.getLogger("urllib3")
log.setLevel(logging.DEBUG)


def _is_successful(response) -> bool:
    """Custom condition.

    Gets the  the return value of the poll function.
    Should return True (truthiness) to stop polling.
    """
    return response.status_code == 200


def _custom_step(step: float) -> float:
    log.debug(f"step %f", step)
    return step + 0.5


def test_polling_basics():
    response = polling.poll(
        lambda: requests.get("http://google.com").status_code == 200,
        step=0.5,  # time to wait between function calls in seconds
        poll_forever=True,  # retry until success or an exception occurred
    )
    # 'poll' returns first value of polling function
    assert response.reason == "OK"


def test_polling_raise_timeout_exception():
    with pytest.raises(polling.TimeoutException):
        polling.poll(
            lambda: requests.get("http://google.com").status_code == 400,
            step=0.5,
            timeout=1,  # total time in seconds
        )


def test_polling_raise_max_call_exception():
    with pytest.raises(polling.MaxCallException):
        polling.poll(
            lambda: requests.get("http://google.com").status_code == 400,
            step=0.5,
            max_tries=3,  # maximum number of retries
        )


def test_polling_custom_condition():
    polling.poll(
        lambda url: requests.get(url),
        kwargs={
            "url": "http://google.com",
        },  # keyword args to be passed to function
        check_success=_is_successful,
        step=0.5,
        poll_forever=True,
    )


def test_polling_custom_step():
    """to test set '--log-cli-level DEBUG' on cmd. line"""
    with pytest.raises(polling.MaxCallException):
        polling.poll(
            lambda: requests.get("http://google.com").status_code == 400,
            step_function=_custom_step,  # adds 0.5 seconds to each iteration
            # step_function=polling.step_constant, #  returns step
            # step_function=polling.step_linear_double,  # returns step * 2
            step=0.5,
            max_tries=3,
        )


def test_polling_ignore_exceptions():
    with pytest.raises(polling.MaxCallException):
        response = polling.poll(
            lambda: requests.get("INVALID_SCHEMA://google.com").status_code == 400,
            ignore_exceptions=(requests.exceptions.InvalidSchema,),
            step=0.5,
            max_tries=3,
        )
        assert response is None


def test_polling_collect_values():
    queue_ = queue.Queue()
    with pytest.raises(polling.MaxCallException):
        polling.poll(
            lambda: requests.get("http://google.com").status_code == 400,
            collect_values=queue_,
            step=0.5,
            max_tries=3,
        )
    # queue_ contains (False, False, False)
