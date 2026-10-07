import pytest
from django.urls import reverse

from accounts.models import Shopper


@pytest.fixture
def user(db):
    return Shopper.objects.create_user(email="patrick@example.com", password="123456789")


def test_valid_login_redirects_and_shows_profile_link(client, user):
    data = {"email": "patrick@example.com", "password": "123456789"}

    response = client.post(reverse("accounts:login"), data=data)
    assert response.status_code == 302

    response = client.get(reverse("index"))
    assert "My profile" in response.content.decode()


def test_invalid_login_shows_login_page_again(client, user):
    data = {"email": "patrick@example.com", "password": "wrong-password"}

    response = client.post(reverse("accounts:login"), data=data)

    assert response.status_code == 200
    assert "accounts/login.html" in [t.name for t in response.templates]


def test_anonymous_user_is_redirected_from_cart(client, db):
    response = client.get(reverse("store:cart"))

    assert response.status_code == 302
    assert "login" in response.url