from django.shortcuts import render
from django.http import HttpResponse
from .models import Review

# Create your views here.
def index(request):
    """
    리뷰 출력
    """
    return HttpResponse("Hello World")