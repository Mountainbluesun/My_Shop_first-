import pytest
from django.urls import reverse
from accounts.models import Shopper
from store.models import Cart, Order, Product

@pytest.fixture
def user_with_cart(db):
    user = Shopper.objects.create_user(email="buyer@example.com", password="123456789")
    product = Product.objects.create(name="Shoes", price=50, stock=10)
    user.add_to_cart(product.slug)
    return user

def test_cart_is_emptied_after_successful_checkout(client, user_with_cart):
    client.force_login(user_with_cart)

    client.get(reverse("store:checkout-success"))

    assert not Cart.objects.filter(user=user_with_cart).exists()
    assert Order.objects.get(user=user_with_cart).ordered
