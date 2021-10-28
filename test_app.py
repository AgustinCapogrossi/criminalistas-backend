from fastapi.testclient import TestClient
from app import app
import random
import string

client = TestClient(app)


def get_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


# Creation new user
def test_create_user():
    rstr = get_random_string(8)
    register = client.post(
        "/creationuser",
        headers={"user_to_create": "pepe"},
        json={
            "username": "german".format(rstr),
        },
    )
    assert register.status_code == 200
