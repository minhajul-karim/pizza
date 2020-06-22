"""View of index page."""

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render

# Create your views here.


def index(request):
    """Home page."""
    return render(request, "orders/index.html")
