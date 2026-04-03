from django.test import TestCase
from django.urls import reverse

from accounts.models import Shopper
from store.models import Product


class StoreTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Sneakers BlueMountain",
            price=10,
            stock=10,
            description="The sneakers is great.",
        )

    def test_product_are_show_on_index_page(self):
        r = self.client.get(reverse("index"))

        self.assertEqual(r.status_code, 200)
        self.assertIn(self.product.name, str(r.content))
        self.assertIn(self.product.thumbnail_url(), str(r.content))

    def test_connection_link_show_when_user_not_connected(self):
        r = self.client.get(reverse('index'))
        self.assertIn("Connection", str(r.content))

    def test_redirect_when_anonymous_user_access_cart_view(self):
        r = self.client.get(reverse("store:cart"))
        self.assertEqual(r.status_code, 302)
        self.assertRedirects(r, f"{reverse('accounts:login')}next={reverse('store:cart')}", status_code=302)


class StoreLoggedInTest(TestCase):
    def setUp(self):
        self.user = Shopper.objects.create_user(
            email="patrick@gmail.com",
            first_name="Patrick",
            last_name="Smith",
            password="123456789"
        )

    def test_valid_login(self):
        data = {'email': 'patrick@gmail.com', 'password': '123456789'}
        r = self.client.post(reverse('accounts:login'), data=data)
        self.assertEqual(r.status_code, 302)
        r = self.client.get(reverse('index'))
        self.assertIn("My profile", str(r.content))

    def test_invalid_login(self):
        data = {'email': 'patrick@gmail.com', 'password': '1234'}
        r = self.client.post(reverse('accounts:login'), data=data)
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "accounts/login.html")

    def test_profile_change(self):
        self.client.login(email="patrick@gmail.com",
                          password="123456789")
        data = {"email": "patrick@gmail.com",
                "password": "123456789",
                "first_name": "Patrick",
                "last_name": "Martin"
                }
        r = self.client.post(reverse('accounts:profile'), data=data)
        self.assertEqual(r.status_code, 302)
        patrick = Shopper.objects.get(email="patrick@gmail.com")
        self.assertEqual(patrick.last_name, "Martin")

