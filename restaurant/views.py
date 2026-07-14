# from django.shortcuts import render
import json
import os

import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from dotenv import load_dotenv
from stripe.params.checkout._session_create_params import (
    SessionCreateParams,
    SessionCreateParamsLineItem,
)

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
        data = json.loads(request.body)
        line_items: list[SessionCreateParamsLineItem] = list(
            map(
                lambda item: {"price": item["stripeId"], "quantity": item["quantity"]},
                data,
            )
        )
        checkout_session = client.v1.checkout.sessions.create(
            params={
                "line_items": line_items,
                "mode": "payment",
                "success_url": DOMAIN + "?success=true",
            }
        )
        return JsonResponse({"url": checkout_session.url})
    except Exception as e:
        return JsonResponse({"message": str(e)})
