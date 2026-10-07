import pytest

from accounts.models import Shopper
from store.models import Cart, Product


@pytest.fixture
def user(db):
    return Shopper.objects.create_user(email="buyer@example.com", password="123456789")


@pytest.fixture
def product(db):
    return Product.objects.create(name="Shoes", price=50, stock=10)


def test_add_to_cart_creates_cart_and_order(user, product):
    user.add_to_cart(product.slug)

    cart = Cart.objects.get(user=user)
    assert cart.orders.count() == 1
    assert cart.orders.first().quantity == 1


def test_adding_same_product_twice_increases_quantity(user, product):
    user.add_to_cart(product.slug)
    user.add_to_cart(product.slug)

    cart = Cart.objects.get(user=user)
    assert cart.orders.count() == 1
    assert cart.orders.first().quantity == 2