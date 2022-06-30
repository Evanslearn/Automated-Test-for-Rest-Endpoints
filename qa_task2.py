# ----- IN TERMINAL, TO TEST MY FILE (MUST CD TO SCRATCH FILE DIRECTORY) -----
# python -m pytest
# py.test -v -rP (rP shows our print statements
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
import requests
import pytest


# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- ----- DEFINITIONS START ----- -----
rolelist = [
    "reporter",
    "executor",
    "admin"
]


successful_login_request_body = {
        "email": "admin@ekmechanes.com",
        "password": "Password!!!!!"
}

successful_login_response_body_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NTY3OTcwNzYsIm5iZiI6MTU1Njc5"\
                                       +"NzA3NiwianRpIjoiNjhkNzRhZDYtNzY1Yy00MWEwLWJiNWYtMmEwMzE2YjFkNmY0IiwiZXhwIj"\
                                       +"oxNTU2ODgzNDc2LCJpZGVudGl0eSI6eyJ1c2VyX2lkIjoiNWNhNWRkZDIzYmY3NzU0NjU0M2"\
                                       +"UyYzlmIiwib3duZXJfaWQiOiI1Y2Ejc3NTQ2NTQzZTJjOWYiLCJzY29wZSI6ImFkbWluX3VzZXIif"\
                                       +"SwiZnJlc2giOnRydWUsInR5cGUiOiJhY2Nlc3MifQ.b6Jd-_cW_l52FHEiwxJtgbaoXKpiKARlALB5"\
                                       +"m672o7Q"
successful_login_response_body = {
        "data": {
            "jwt": {
                "accessToken": successful_login_response_body_token
            }
        },
        "status": "200"
}


unsuccessful_login_request_body = {
        "email": "admin@ekmechanes.com",
        "password": "P4ssword!!!!!"
}

unsuccessful_login_response_body = {
        "error": {
            "messages": [
                "Invalid username-password combination."
            ]
        },
        "status": "400"
}


successful_updateuser_request_body = {}
for i in range(0,3):
    successful_updateuser_request_body[i] = {
        "email": "admin@ekmechanes.com",
        "role": rolelist[i],
        "active": False
    }

successful_updateuser_response_body = {}
for i in range(0,3):
    successful_updateuser_response_body[i] = {
            "data": {
                "user": {
                    "active": False,
                    "createdAt": "2019-04-04 10:34:58.981000",
                    "createdBy": "5c6d11513bf77553560b6a4d",
                    "email": "admin@ekmechanes.com",
                    "id": "5ca5ddd23bf77546543e2c9f",
                    "passwordChanged": False,
                    "role": rolelist[i],
                    "updatedAt": "2019-05-02 11:56:17.624482",
                    "updatedBy": "5ca5ddd23bf77546543e2c9f"
                }
            },
            "status": "200"
    }
# ----- ----- DEFINITIONS END ----- -----
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----


# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- ----- Login Testing START ----- -----
host = "0.0.0.0:8000"
url1_help = "/api/v1/authentication/login"
url1 = host + url1_help
url2_help = "/api/v1/users/5ca5ddd23bf77546543e2c9f"
url2 = host + url2_help
#testurl = 'https://reqres.in/api/login'
#testurl2 = 'https://reqres.in/api/users/2'


def check_successful_login_response(response_body):

    #print(requests.__version__)
    key0 = "status"
    key1 = "data"
    key2 = "jwt"
    key3 = "accessToken"

    assert isinstance(response_body, dict), f"{response_body} is not a dictionary"
    assert (key1 in response_body.keys()), f"{key1} not in response body keys"
    assert (key2 in response_body[key1].keys()), f"{key2} not in response body keys"
    assert (key3 in response_body[key1][key2].keys()), f"{key3} not in response body keys"
    assert (key0 in response_body.keys()), f"{key0} not in response body keys"

    token = response_body[key1][key2][key3]
    status = response_body[key0]
    return token, status


@pytest.mark.parametrize("url,request_body",  [(url1, successful_login_request_body)])
def test_successful_login(url, request_body):

    response = requests.post(url, json = request_body)
    response_body = response.json()
    #response_body = successful_login_response_body

    (token, status) = check_successful_login_response(response_body)

    assert isinstance(token, str), f"Login did not return a token: \n{token}."
    assert status == "200", f"Our login was not successful (status code = {status})"


def check_unsuccessful_login_response(response_body):

    key0 = "status"
    key1 = "error"
    key2 = "messages"
    assert isinstance(response_body, dict), f"{response_body} is not a dictionary"
    assert (key1 in response_body.keys()), f"{key1} not in response body keys"
    assert (key2 in response_body[key1].keys()), f"{key2} not in response body keys"
    assert (key0 in response_body.keys()), f"{key0} not in response body keys"

    message = (response_body[key1][key2])[0]
    status = response_body[key0]
    return message, status


@pytest.mark.parametrize("url,request_body",  [(url1, unsuccessful_login_request_body)])
def test_unsuccessful_login(url, request_body):

    response = requests.post(url, json = request_body)
    response_body = response.json()
    #response_body = unsuccessful_login_response_body

    (message, status) = check_unsuccessful_login_response(response_body)
    assert message == "Invalid username-password combination.", "Message not 'Invalid username-password combination.'"
    assert status == "400", "Status code not 400"
# ----- ----- Login Testing END ----- -----
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----


# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- ----- UPDATE USER START ----- -----
def check_successful_updateuser_response(response_body):

    key0 = "status"
    key1 = "data"
    key2 = "user"
    key3 = "role"
    assert isinstance(response_body, dict), f"{response_body} is not a dictionary"
    assert (key1 in response_body.keys()), f"{key1} not in response body keys"
    assert (key2 in response_body[key1].keys()), f"{key2} not in response body keys"
    assert (key3 in response_body[key1][key2].keys()), f"{key3} not in response body keys"

    # Here we could also write the solution using recursion
    if isinstance(response_body[key1][key2], dict):
        for key in response_body[key1][key2].keys():
            assert (key in response_body[key1][key2].keys()), f"{key} not in response body keys"

    assert (key0 in response_body.keys()), f"{key0} not in response body keys"

    role = (response_body[key1][key2][key3])
    status = response_body[key0]
    return role, status


token_header = {"Authorization": "Bearer_token"}
successful_updateuser_request_body_allroles = list()
for i in range(0, 3):
    successful_updateuser_request_body_allroles.append(
        (url2, token_header, successful_updateuser_request_body[i])
    )
myparams = successful_updateuser_request_body_allroles


@pytest.mark.parametrize("url,token,request_body",  myparams)
def test_sucessful_updateuser(url, request_body, token):

    response = requests.put(url, headers = token, json = request_body)
    response_body = response.json()
    #response_body = successful_updateuser_response_body[2]

    (role, status) = check_successful_updateuser_response(response_body)

    assert status == "200", 'Status was not equal to 200'
    assert (role == "executor" or role == "admin" or role == "reporter"), f"Error code: 400.\nRole: {role} is invalid"
# ----- ----- UPDATE USER END ----- -----
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
