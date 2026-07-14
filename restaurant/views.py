# from django.shortcuts import render
import json
import os

import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from dotenv import load_dotenv

load_dotenv()

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
if STRIPE_SECRET_KEY is None:
    raise Exception("STRIPE_SECRET_KEY not set")

DOMAIN = os.getenv("DOMAIN")
if DOMAIN is None:
    raise Exception("DOMAIN not set")

client = stripe.StripeClient(STRIPE_SECRET_KEY)


# Create your views here.
def root(request):
    return JsonResponse({"message": "Hello Django"})


@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({"message": "CSRF cookie set"})


def checkout(request):
    try:
        # data = json.loads(request.body)
        print("bruh")
        print("bruh")
        # print(data)
        print("bruh")
        print("bruh")
        print("bruh")
        checkout_session = client.v1.checkout.sessions.create(
            params={
                "line_items": [
                    {
                        # Provide the exact Price ID (for example, price_1234) of the product you want to sell
                        "price": "price_1TtDpCGxknssnJ80Jjic4GPE",
                        "quantity": 1,
                    },
                ],
                "mode": "payment",
                "success_url": DOMAIN + "?success=true",
            }
        )
        print()
        print(checkout_session.url)
        print()
        return JsonResponse({"url": checkout_session.url})
    except Exception as e:
        return JsonResponse({"message": str(e)})
