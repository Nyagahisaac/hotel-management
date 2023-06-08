from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
from datetime import datetime
from ..models import Configurations,ConfigurationTypes

def index(request):
    '''serve configuration types an d actual configurations'''
    types = ConfigurationTypes.objects.all()
    return render(request,'configurations/index.html',{"types":types})

def maintainConfigurationTypes(request):
    '''Mainatain configuration types'''
    c_type = ConfigurationTypes.objects.get(id=request.POST['type_id']) if ConfigurationTypes.objects.filter(id=request.POST['type_id']).first() else ConfigurationTypes()
    c_type.name = request.POST['name']
    c_type.created_by = request.user
    c_type.save()
    
    messages.info(request,'Configuration type updated successfully')
    return redirect(request.META['HTTP_REFERER'])

def maintainConfigurationData(request):
    '''Manage configuration data'''
    config = Configurations.objects.get(id=request.POST['config_id']) if Configurations.objects.filter(id=request.POST['config_id']).first() else Configurations()
    config.config_type = ConfigurationTypes.objects.get(id=request.POST['config_type_id'])
    config.key = request.POST['key']
    config.value = request.POST['value']
    config.save()
    
    messages.info(request,'Configuration data updated successfully')
    return redirect(request.META['HTTP_REFERER'])

def deleteConfigurationType(request):
    '''delete configuration type'''
    c_type = ConfigurationTypes.objects.get(id=request.POST['c_type_id'])
    c_type.delete()
    
    messages.info(request,'Configuration Type deleted successfully')
    return redirect(request.META['HTTP_REFERER'])

def deleteConfigurationData(request):
    '''delete configuration type'''
    config = Configurations.objects.get(id=request.POST['config_id'])
    config.delete()
    
    messages.info(request,'Configuration data deleted successfully')
    return redirect(request.META['HTTP_REFERER'])