import pytest
import stripe
from django.urls import reverse

from accounts.models import ShippingAddress, Shopper
from store.models import Cart, Order, Product


@pytest.fixture
def user(db):
    return Shopper.objects.create_user(email="buyer@example.com", password="123456789")


@pytest.fixture
def user_with_cart(user):
    product = Product.objects.create(name="Shoes", price=50, stock=10)
    user.add_to_cart(product.slug)
    return user


@pytest.fixture
def completed_event(user):
    return {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "customer": "cus_test_123",
                "customer_details": {"email": user.email},
                "shipping": {
                    "name": "Jane Doe",
                    "address": {
                        "city": "Lyon",
                        "country": "FR",
                        "line1": "1 Rue Test",
                        "line2": None,
                        "postal_code": "69000",
                    },
                },
            }
        },
    }


def post_webhook(client, **headers):
    return client.post(
        reverse("store:stripe-webhook"),
        data="{}",
        content_type="application/json",
        **headers,
    )


def test_webhook_rejects_invalid_signature(client, db):
    response = post_webhook(client, HTTP_STRIPE_SIGNATURE="t=1,v1=invalid")

    assert response.status_code == 400


def test_webhook_rejects_missing_signature_header(client, db):
    response = post_webhook(client)

    assert response.status_code == 400


def test_webhook_finalises_order_and_saves_stripe_id(client, monkeypatch, user_with_cart, completed_event):
    monkeypatch.setattr(stripe.Webhook, "construct_event", lambda *args, **kwargs: completed_event)

    response = post_webhook(client, HTTP_STRIPE_SIGNATURE="t=1,v1=fake")

    assert response.status_code == 200
    assert not Cart.objects.filter(user=user_with_cart).exists()
    assert Order.objects.get(user=user_with_cart).ordered
    user_with_cart.refresh_from_db()
    assert user_with_cart.stripe_id == "cus_test_123"
    assert ShippingAddress.objects.filter(user=user_with_cart).count() == 1


def test_webhook_does_not_crash_when_cart_is_already_gone(client, monkeypatch, user, completed_event):
    monkeypatch.setattr(stripe.Webhook, "construct_event", lambda *args, **kwargs: completed_event)

    response = post_webhook(client, HTTP_STRIPE_SIGNATURE="t=1,v1=fake")

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.stripe_id == "cus_test_123"