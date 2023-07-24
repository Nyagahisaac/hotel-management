from django.shortcuts import render

from django.urls import reverse_lazy

from django.views.generic import CreateView

from django.contrib.auth.models import User

from ..models import Bookings

def bookings_view(request):
    bookings = Bookings.objects.all()
    return render(request, 'bookings/index.html', {'bookings': bookings})


def home(request):
    return render(request, "home.html", {})

