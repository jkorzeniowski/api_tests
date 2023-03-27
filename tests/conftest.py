import string
import random
from typing import Union

import pytest
import requests

from variables import ENDPOINT, REQUEST_TIMEOUT_GLOBAL


def random_string_generator(length: int) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def create_user() -> dict:
    user_data = {
        "name": random_string_generator(6),
        "job": random_string_generator(6)
    }

    response = requests.post(f"{ENDPOINT}/api/users", json=user_data, timeout=REQUEST_TIMEOUT_GLOBAL)
    assert response.status_code == 201, f"Something went wrong, actual status code: {response.status_code}\n" \
                                        f"while expected code: 201"
    user_data = response.json()
    return user_data


def delete_user(user_id: Union[int, str]):
    if isinstance(user_id, str):
        assert user_id.isnumeric()

    response = requests.delete(f"{ENDPOINT}/api/users/{user_id}", timeout=REQUEST_TIMEOUT_GLOBAL)
    assert response.status_code == 204, f"Something went wrong, actual status code: {response.status_code}\n" \
                                        f"while expected code: 204"


@pytest.fixture()
def user_setup():
    user_data = create_user()
    yield user_data
    delete_user(user_id=user_data['id'])
