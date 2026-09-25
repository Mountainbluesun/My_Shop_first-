🌿 The Nature Shop

A robust e-commerce application built with Django 5.1, featuring a custom authentication system and full Stripe checkout integration.

🚀 Key Features

**Custom Authentication:** Uses a Shopper model based on email as the unique identifier (instead of the classic username).

**Cart Management:** Add, update, and remove items in real time.

**Stripe Integration:** Secure checkout flow with checkout session handling and success/cancel pages.

**Clean Architecture:** Clear separation between business logic (store), authentication (accounts), and global configuration.

## 📸 Project Preview

### Cart & Catalog

[![Cart and Items](https://github.com/Mountainbluesun/My_Shop_first-/raw/main/screenshots/screenshot_cart_anonyme.png)](/Mountainbluesun/My_Shop_first-/blob/main/screenshots/screenshot_cart_anonyme.png)

### Secure Payment via Stripe

[![Stripe Interface](https://github.com/Mountainbluesun/My_Shop_first-/raw/main/screenshots/fictitious_Stripe_payment_history.png)](/Mountainbluesun/My_Shop_first-/blob/main/screenshots/fictitious_Stripe_payment_history.png)

### Order Confirmation

[![Payment Success](https://github.com/Mountainbluesun/My_Shop_first-/raw/main/screenshots/screenshot_success_anonyme.png)](/Mountainbluesun/My_Shop_first-/blob/main/screenshots/screenshot_success_anonyme.png)

### Terminal Log

[![Success log](https://github.com/Mountainbluesun/My_Shop_first-/raw/main/screenshots/Log_terminal_checkout_session_ok.png)](/Mountainbluesun/My_Shop_first-/blob/main/screenshots/Log_terminal_checkout_session_ok.png)

🛠️ Tech Stack

**Framework:** Django 5.1.4

**Database:** SQLite (ideal for development and demo purposes)

**Payments:** Stripe API (python-stripe)

**Environment:** Python 3.12 + Virtualenv