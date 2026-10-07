from types import SimpleNamespace

import pytest
import stripe
from django.urls import reverse

from accounts.models import Shopper
from store.models import Cart, Order, Product


@pytest.fixture
def user_with_cart(db):
    user = Shopper.objects.create_user(email="buyer@example.com", password="123456789")
    product = Product.objects.create(name="Shoes", price=50, stock=10)
    user.add_to_cart(product.slug)
    return user


def mock_stripe_session(monkeypatch, user, payment_status="paid"):
    session = SimpleNamespace(
        payment_status=payment_status,
        client_reference_id=str(user.pk),
    )
    monkeypatch.setattr(stripe.checkout.Session, "retrieve", lambda *args, **kwargs: session)


def test_cart_is_emptied_after_paid_checkout(client, monkeypatch, user_with_cart):
    mock_stripe_session(monkeypatch, user_with_cart)
    client.force_login(user_with_cart)

    client.get(reverse("store:checkout-success"), {"session_id": "cs_test_123"})

    assert not Cart.objects.filter(user=user_with_cart).exists()
    assert Order.objects.get(user=user_with_cart).ordered


def test_cart_is_kept_when_session_is_not_paid(client, monkeypatch, user_with_cart):
    mock_stripe_session(monkeypatch, user_with_cart, payment_status="unpaid")
    client.force_login(user_with_cart)

    client.get(reverse("store:checkout-success"), {"session_id": "cs_test_123"})

    assert Cart.objects.filter(user=user_with_cart).exists()
    assert not Order.objects.get(user=user_with_cart).ordered


def test_cart_is_kept_when_session_belongs_to_another_user(client, monkeypatch, user_with_cart):
    other = Shopper.objects.create_user(email="other@example.com", password="123456789")
    mock_stripe_session(monkeypatch, other)
    client.force_login(user_with_cart)

    client.get(reverse("store:checkout-success"), {"session_id": "cs_test_123"})

    assert Cart.objects.filter(user=user_with_cart).exists()


def test_cart_is_kept_when_session_id_is_missing(client, user_with_cart):
    client.force_login(user_with_cart)

    client.get(reverse("store:checkout-success"))

    assert Cart.objects.filter(user=user_with_cart).exists()