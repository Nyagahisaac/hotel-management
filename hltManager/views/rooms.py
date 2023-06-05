from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import datetime
from datetime import datetime

from ..models import RoomsHeader,RoomDetails

def maintainRoomTypes(request):
    '''Maintains Room Types Data'''
    
    r_type = RoomsHeader.objects.get(id=request.POST['room_type_id']) if request.POST['room_type_id'] > 0 else RoomsHeader()
    r_type.basic_rent = request.POST['basic_rent']
    r_type.code = request.POST['code']
    r_type.name = request.POST['name']
    r_type.created_by = request.user
    r_type.save()
    messages.info(request,'Room type(s) records updated successfully')
    
    return redirect(request.META['HTTP_REFERER'])

def deleteRoomType(request):
    '''Delete Room Type data'''
    r_type = RoomsHeader.objects.get(id=request.POST['room_type_id'])
     
    r_type.deleted_at =datetime.today()
    r_type.save()
    messages.info(request,'Room type(s) records deleted successfully')
    return redirect(request.META['HTTP_REFERER'])

def maintainRoomsData(request):
    '''Maintain rooms data'''
    room_type = RoomsHeader.objects.get(id=request.POST['room_type_id'])
    room = RoomDetails.objects.get(id=request.POST['room_id']) if request.POST['room_id'] > 0 else RoomDetails()
    if  not RoomDetails.objects.get(id=request.POST['room_id']):
        record_count = RoomDetails.objects.filter(room_type_id = request.POST['room_type_id']).count()
        counter = record_count + 1 if record_count > 0 else 1
        if len(str(counter)) < 3 :
            zero_counter = 3 - len(str(counter)) * 0
            actualcode = f'{room_type.code}/RM{zero_counter}{str(counter)}'.upper()
        else:
            actualcode = f'{room_type.code}/RM{str(counter)}'.upper()
        room.code = actualcode  
        room.room_no = counter
    room.basic_rent = request.POST['basic_rent']
    room.bed_capacity = request.POST['bed_capacity']
    room.created_by = request.user
    room.meal = Configurations.objects.get(id=request.POST['meal_id'])
    room.name = request.POST['name']
    room.room_type = room_type
    room.status = Configurations.objects.get(id=request.POST['status_id'])
    room.save()
    
    messages.info(request,'Room (s) records updated successfully')
    return redirect(request.META['HTTP_REFERER'])

def changeRoomStatus(request):
    status = Configurations.objects.get(id=request.POST['status_id'])
    for room_id in request.POST.getlist('room_ids'):
        room = RoomDetails.objects.get(id=request.POST['room_id'])
        room.status = status
        room.save()
    messages.info(request,'Room (s) Status updated successfully')
    return redirect(request.META['HTTP_REFERER'])        
    