import stripe

from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_stripe_price(obj):
    return stripe.Price.create(
        currency="rub",
        unit_amount=int(obj.price) * 100,
        product_data={"name": obj.title},
    )


def create_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def create_stripe_product(name):
    return stripe.Product.create(name=name).get("id")
