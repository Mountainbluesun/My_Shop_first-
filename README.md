# The Nature Shop

![Tests](https://github.com/Mountainbluesun/My_Shop_first-/actions/workflows/tests.yml/badge.svg)

A small e-commerce demo built with Django 5.2: email-based authentication, a shopping cart, and a Stripe Checkout payment flow.

## Features

- **Email authentication:** a custom `Shopper` user model that logs in with an email address instead of a username.
- **Shopping cart:** add products, change quantities, and remove items.
- **Shipping addresses:** each user can save and manage delivery addresses.
- **Stripe Checkout:** hosted payment page created from the cart, with success and cancel pages. The cart is emptied after a successful payment.
- **Tests and CI:** pytest tests, run automatically by GitHub Actions on every push.

## Screenshots

### Cart

[![Cart](screenshots/screenshot_cart_anonyme.png)](screenshots/screenshot_cart_anonyme.png)

### Order confirmation

[![Order confirmation](screenshots/screenshot_success_anonyme.png)](screenshots/screenshot_success_anonyme.png)

## Tech stack

- Python 3.12
- Django 5.2
- SQLite
- Stripe API (`stripe` Python package)
- Pillow, django-environ, iso3166
- pytest and pytest-django

## Getting started

```bash
git clone https://github.com/Mountainbluesun/My_Shop_first-.git
cd My_Shop_first-
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and fill in your own values:

- `SECRET_KEY`: any long random string
- `STRIPE_API_KEY`: a secret key from your Stripe account (test mode)
- `ENDPOINT_SECRET`: a Stripe webhook signing secret

Then create the database and start the server:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Create your products in the Django admin at `/admin/`. Each product needs the ID of a Stripe price (`price_...`) created in your Stripe dashboard, otherwise checkout cannot bill it.

## Running the tests

```bash
pip install pytest pytest-django
pytest
```

## Payments and webhooks

- Payment is verified when the customer returns to the success page: the server retrieves the Stripe Checkout Session and only empties the cart if the session is paid and belongs to the logged-in user.
- A Stripe webhook endpoint (`/boutique/stripe-webhook/`) also finalises the order when `checkout.session.completed` is received. It verifies the Stripe signature, saves the Stripe customer ID and the shipping address, and empties the cart.
- To receive webhooks on a local server, use the Stripe CLI: `stripe listen --forward-to localhost:8000/boutique/stripe-webhook/`. It prints the signing secret to put in `ENDPOINT_SECRET`.
- The webhook is covered by automated tests that simulate Stripe, but it has not been exercised against a real Stripe event stream.

## Limitations

- Demo project: Stripe runs in test mode only, with SQLite as the database.