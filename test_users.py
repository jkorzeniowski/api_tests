import requests
from variables import ENDPOINT, REQUEST_TIMEOUT_GLOBAL


def test_get_user_list():
    response = requests.get(f"{ENDPOINT}api/users", timeout=REQUEST_TIMEOUT_GLOBAL)
    assert response.status_code == 200, f"Something went wrong, actual status code: {response.status_code}\n" \
                                        f"while expected code: 200"


def test_get_user_data_section():
    expected_first_user = {
        'id': 1, 'email': 'george.bluth@reqres.in', 'first_name': 'George',
        'last_name': 'Bluth', 'avatar': 'https://reqres.in/img/faces/1-image.jpg'
    }
    response = requests.get(f"{ENDPOINT}api/users/1", timeout=REQUEST_TIMEOUT_GLOBAL)
    assert response.status_code == 200, f"Something went wrong, actual status code: {response.status_code}\n" \
                                        f"while expected code: 200"
    assert response.json(), "No JSON in the response"

    data_dict = response.json()['data']
    assert data_dict == expected_first_user, "First user data differs. User data updated/changed.\n" \
                                             f"Expected data: {expected_first_user}\n" \
                                             f"Actual data: {data_dict}"


def test_get_user_support_section():
    expected_support_section = {
        'url': 'https://reqres.in/#support-heading',
        'text': 'To keep ReqRes free, contributions towards server costs are appreciated!'
    }

    response = requests.get(f"{ENDPOINT}api/users/1", timeout=REQUEST_TIMEOUT_GLOBAL)
    assert response.status_code == 200, f"Something went wrong, actual status code: {response.status_code}\n" \
                                        f"while expected code: 200"
    assert response.json(), "No JSON in the response"

    support_section = response.json()['support']
    assert support_section == expected_support_section, "Help section differs. Help section updated/changed.\n" \
                                                        f"Expected data: {expected_support_section}\n" \
                                                        f"Actual data: {support_section}"


def test_get_invalid_user():
    response = requests.get(f"{ENDPOINT}api/users/999", timeout=REQUEST_TIMEOUT_GLOBAL)
    assert response.status_code == 404, f"Something went wrong, " \
                                        f"expected code: 404, while actual code was {response.status_code}"

    assert not response.json(), "JSON was available in the response but not expected any"
