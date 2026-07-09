# from django.shortcuts import render
import json

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie


# Create your views here.
def root(request):
    return JsonResponse({"message": "Hello Django"})


@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({"message": "CSRF cookie set"})


# @csrf_exempt
def submit_order(request):
    if request.method == "POST":
        # data = json.loads(request.body)
        # print(data)
        return JsonResponse({"message": "Order received!"})
    return JsonResponse({"message": "Invalid Request"})
