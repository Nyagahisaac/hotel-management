from django.shortcuts import render

from django.urls import reverse_lazy

from django.views.generic import CreateView


from django.contrib.auth.models import User


class  Bookings(CreateView):


    template_name = 'templates/bookings/index.html'

def home(request):

    return render(request, "home.html", {})