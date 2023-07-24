from django.shortcuts import render, redirect, get_object_or_404
from ..models import *
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.utils.timezone import datetime  # important if using timezones
from datetime import timedelta
from django.core.files.storage import FileSystemStorage

def login_user_data(request):
    if request.method == 'GET':
        return render(request,'auth/login.html')
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        if user.is_staff == False:
            logout(request)
            messages.info(request,'You not authorised to access the system')
            return redirect(request.META['HTTP_REFERER'])

        login(request, user)
        randomlist = random.sample(range(1, 9), 6)
        randomStr = map(str, randomlist)
        otpcode = ''.join(randomStr)
        message = 'Your verification code is {}'.format(otpcode)
        user.profile.otp = otpcode
        user.profile.otp_verified = False
        user.save()
        subject = 'Hotel Verification Code'
        sendmail(subject,message,request.POST['username'])
        return redirect('/')        # A backend authenticated the credentials
    else:
        messages.info(request,'Invalid credentials')
        return redirect(request.META['HTTP_REFERER'])
    
def verification_user(request):
    if request.method == 'POST':
        code = request.POST['verification']
        if request.user.profile.otp == code:
            request.user.profile.otp_verified = True
            request.user.profile.save()
            return redirect('hotel:loadDashoardHome')
        else:
            messages.info(request,'Invalid token')
            return render(request,'login/verify.html')
    else:
        return render(request,'login/verify.html')    
    
def logout_view(request):
    request.user.profile.otp = ''
    request.user.profile.otp_verified = False
    request.user.save()
    logout(request)

    return redirect('hotel:loadDashoardHome')  


def add_staff_user(request):
    # return HttpResponse(User.objects.filter(email=request.POST['email']).first())
    if User.objects.filter(username=request.POST['email']).first() and request.POST['user_id'] == '0':
        messages.info(request,'There is a user with specified email address')
        return redirect(request.META['HTTP_REFERER'])
    elif int(request.POST['user_id'] ) > 0:
        check_user = User.objects.filter(id=request.POST['user_id']).first()
        user =User.objects.filter(username=request.POST['email']).first()
        if user.id != check_user.id:
            messages.info(request,'There is a user with specified email address')
            return redirect(request.META['HTTP_REFERER'])
    if request.POST['password'] != request.POST['confirm_password'] and request.POST['user_id'] == '0':
        messages.info(request,'Passwords not matching')
        return redirect(request.META['HTTP_REFERER'])

    user = User.objects.filter(id=request.POST['user_id']).first() if User.objects.filter(id=request.POST['user_id']).first() else User()
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.username = request.POST['email']
    if request.POST['password'] != '':
        
        user.set_password(request.POST['password'])
    
    user.is_staff = True
    user.is_active = True if 'is_active' in request.POST else False
    user.save()
    
    user.profile.phone_number = request.POST['phone_number']
    if 'photo_url' in request.FILES:
        file_data = base64.b64encode(request.FILES['photo_url'].read())
        user.profile.photo_url = file_data.decode('UTF_8')
    if 'signature' in request.FILES:
        signature = base64.b64encode(request.FILES['signature'].read())
        user.profile.signature_url = signature.decode('UTF_8')
    user.profile.gender_id = request.POST['gender']
    user.profile.id_number = request.POST['id_number']
    user.save()
    # staff_group = Configurations.objects.filter(name='staff_id').first()
    # group_staff = getGroupByID(staff_group.code)
    # group_staff.user_set.add(user)
    messages.info(request,'Staff record updated successfully!')
    return redirect('mentorapp:authorization_index')