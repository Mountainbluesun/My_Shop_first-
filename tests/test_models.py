import pytest
from django.urls import reverse
from django.utils import timezone

from accounts.models import Shopper
from store.models import Cart, Order, Product


@pytest.fixture
def product(db):
    return Product.objects.create(name="Blue Mountain Sneakers", price=10, stock=10)


def test_product_slug_is_generated_from_name(product):
    assert product.slug == "blue-mountain-sneakers"


def test_product_absolute_url(product):
    expected = reverse("store:product", kwargs={"slug": product.slug})
    assert product.get_absolute_url() == expected


def test_deleting_cart_marks_orders_as_ordered(product):
    user = Shopper.objects.create_user(email="buyer@example.com", password="123456789")
    cart = Cart.objects.create(user=user)
    order = Order.objects.create(user=user, product=product)
    cart.orders.add(order)

    cart.delete()

    order.refresh_from_db()
    assert order.ordered
    assert order.ordered_date is not None
    assert order.ordered_date <= timezone.now()