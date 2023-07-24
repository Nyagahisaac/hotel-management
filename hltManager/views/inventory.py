from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
from datetime import datetime
from ..models import InventoryHeader,InventoryItems,Configurations

def inventory(request):
    '''Serve the main inventory Categories'''
    headers = InventoryHeader.objects.filter(deleted_at__isnull = True)
    return render(request,'inventory/index.html',{"headers":headers})

def show(request,id):
    '''Serves inventory sub categories or the actual inventory items'''
    details = InventoryItems.objects.filter(inventory_header_id = id,deleted_at__isnull = True)
    header = InventoryHeader.objects.get(id=id)
    return render(request,'inventory/index.html',{"header":header,"details":details})

def manageInventoryHeaders(request):
    '''Manages the inventory main categories'''
    header = InventoryHeader.objects.get(id=request.POST['header_id']) if InventoryHeader.objects.filter(id=request.POST['header_id']).first() else InventoryHeader()
    header.code = request.POST['code']
    header.name = request.POST['name']
    header.created_by = request.user
    header.save()
    
    messages.info(request,'Inventory categories updated successfully')
    
    return redirect(request.META['HTTP_REFERER'])
    
def deleteInventoryHeaders(request):
    '''Delete inventory headers'''
    header = InventoryHeader.objects.get(id=request.POST['header_id'])
    header.deleted_at = datetime.today()
    header.save()
    messages.info(request,'Inventory categories deleted successfully')
    return redirect(request.META['HTTP_REFERER'])

def maintainInventoryDetails(request):
    '''Manages invetory sub categories / items'''
    header = InventoryHeader.objects.get(id=request.POST['header_id'])
    detail = InventoryItems.objects.get(id=request.POST['detail_id']) if InventoryItems.objects.filter(id=request.POST['detail_id']).first() else InventoryItems()
    detail.code = request.POST['code']
    detail.inventory_header_id = header
    detail.name = request.POST['name']
    detail.status = Configurations.objects.get(id=request.POST['status'])
    detail.total_stock = request.POST['total_stock']
    detail.save()
    
    messages.info(request,'Inventory Items updated successfully')
    return redirect(request.META['HTTP_REFERER'])
    
def deleteInvetoryDetails(request):
    '''delete inventory details data'''
    detail = InventoryItems.objects.get(id=request.POST['detail_id'])
    detail.deleted_at = datetime.today()
    detail.save()
    
    messages.info(request,'Inventory Items deleted successfully')
    return redirect(request.META['HTTP_REFERER'])