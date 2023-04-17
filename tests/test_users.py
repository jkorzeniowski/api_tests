import requests
from variables import ENDPOINT, REQUEST_TIMEOUT_GLOBAL


class TestUsers:
    """
    API tests regarding user management.
    """

    def test_get_user_list(self):
        response = requests.get(f"{ENDPOINT}/api/users", timeout=REQUEST_TIMEOUT_GLOBAL)
        assert response.status_code == 200, f"Something went wrong, actual status code: {response.status_code}\n" \
                                            f"while expected code: 200"

    def test_get_user_data_section(self):
        expected_first_user = {
            'id': 1, 'email': 'george.bluth@reqres.in', 'first_name': 'George',
            'last_name': 'Bluth', 'avatar': 'https://reqres.in/img/faces/1-image.jpg'
        }
        response = requests.get(f"{ENDPOINT}/api/users/1", timeout=REQUEST_TIMEOUT_GLOBAL)
        assert response.status_code == 200, f"Something went wrong, actual status code: {response.status_code}\n" \
                                            f"while expected code: 200"
        assert response.json(), "No JSON in the response"
        assert response.json()['data'] == expected_first_user, "First user data differs. User data updated/changed.\n" \
                                                               f"Expected data: {expected_first_user}\n" \
                                                               f"Actual data: {response.json()['data']}"

    def test_get_user_support_section(self):
        response = requests.get(f"{ENDPOINT}/api/users/1", timeout=REQUEST_TIMEOUT_GLOBAL)
        assert response.status_code == 200, f"Something went wrong, actual status code: {response.status_code}\n" \
                                            f"while expected code: 200"
        assert response.json(), "No JSON in the response"

    def test_get_invalid_user(self):
        response = requests.get(f"{ENDPOINT}/api/users/999", timeout=REQUEST_TIMEOUT_GLOBAL)
        assert response.status_code == 404, f"Something went wrong, " \
                                            f"expected code: 404, while actual code was {response.status_code}"

        assert not response.json(), "JSON was available in the response but not expected any."

    def test_create_and_delete_user(self):
        user_data = {
            "name": "Karim",
            "job": "Scientist"
        }
        create_response = requests.post(f"{ENDPOINT}/api/users", json=user_data, timeout=REQUEST_TIMEOUT_GLOBAL)
        create_response_data = create_response.json()
        assert create_response.status_code == 201, f"Something went wrong, actual status code: " \
                                                   f"{create_response.status_code}\n" \
                                                   f"while expected code: 201"
        assert create_response.json(), "Response have no response data (JSON) or response data is invalid"
        assert create_response_data['name'] == user_data['name'], f"Data in response differs.\n" \
                                                                  f"User name in response: {create_response_data['name']}" \
                                                                  f"User name provided: {user_data['name']}"
        assert create_response_data['job'] == user_data['job'], f"Data in response differs.\n" \
                                                                f"User job in response: {create_response_data['job']}" \
                                                                f"User job provided: {user_data['job']}"
        assert create_response_data['id'], "ID for the user not set or not provided in response."
        assert create_response_data['id'].isnumeric(), \
            f"ID for the user is not integer type: ID: {create_response_data['id']}"

        delete_response = requests.delete(f"{ENDPOINT}/api/users/{create_response_data['id']}",
                                          timeout=REQUEST_TIMEOUT_GLOBAL)
        assert delete_response.status_code == 204, f"Something went wrong, actual status code: " \
                                                   f"{delete_response.status_code}\n" \
                                                   f"while expected code: 204"

    def test_update_user(self, user_setup):
        new_user_data = {
            "name": "Tom",
            "job": "Actor"
        }
        response = requests.patch(f"{ENDPOINT}/api/users/{user_setup['id']}", json=new_user_data,
                                  timeout=REQUEST_TIMEOUT_GLOBAL)

        assert response.status_code == 200, f"Something went wrong, actual status code: {response.status_code}\n" \
                                            f"while expected code: 200"
        assert response.json(), "Response have no response data (JSON) or response data is invalid"
