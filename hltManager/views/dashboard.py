from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group, Permission
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

# @login_required(login_url='/login/user/data')

def loadDashoardHome(request):
    '''Loads Backend Dashboard'''
    return render(request,'dashboard/index.html')