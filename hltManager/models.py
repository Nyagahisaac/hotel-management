from django.db import models
from django.contrib.auth.models import User,Group

# Create your models here.
class HotelProfile(models.Model):
    '''
    Manage Hotel Information / Data
    '''
    name = models.CharField(max_length=100,null=False,blank=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @classmethod
    def getHotelByID(cls,id):
        return cls.objects.get(id=id)
    
class Profile(models.Model):
    '''
    manage extra user information / data
    '''
    phone_number = models.CharField(max_length=15,null=False,blank=False)
    otp_code = models.CharField(max_length=10,null=False,blank=False)
    email_verified = models.BooleanField(default=False,null=False,blank=False)
    profile_photo = models.TextField(null=True)
    signature_url = models.TextField(null=True)
    user_id = models.OneToOneField(User, related_name="pr_user_id", on_delete=models.CASCADE,null=False)
    deleted_at = models.DateTimeField(auto_now=False, auto_now_add=False,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user_id.first_name} {self.user_id.last_name}'

class UserRoles(models.Model):
    '''
    Manages User Roles
    '''
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    role_id = models.ForeignKey(Group, related_name="role_id", on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="created_by", on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return f'{self.user_id.first_name} {self.user_id.last_name}'
    
class Configurations(models.Model):
    '''
    Manage system configurations / settings
    '''
    key = models.CharField(max_length=255,null=False,blank=False)
    value = models.CharField(max_length=255,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.key
    
class RoomsHeader(models.Model):
    '''Manages room types'''
    
    name = models.CharField(max_length=255,null=False,blank=False)
    code = models.CharField(max_length=255,null=False,blank=False)
    basic_rent = models.FloatField(null=False)
    deleted_at = models.DateTimeField(auto_now=False, auto_now_add=False,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="room_created_by", on_delete=models.CASCADE,null=False)
    
    def __str__(self):
        return self.name
    
class RoomDetails(models.Model):
    '''Manage room details / data'''    
    name = models.CharField(max_length=255,null=False,blank=False)
    code = models.CharField(max_length=255,null=False,blank=False)
    room_no = models.CharField(max_length=500,null=False,blank=False)
    bed_capacity = models.ForeignKey(Configurations,on_delete=models.CASCADE,null=False)
    meal = models.ForeignKey(Configurations, related_name="cnf_meal", on_delete=models.CASCADE,null=False)
    room_type = models.ForeignKey(RoomsHeader,on_delete=models.CASCADE,null=False)
    basic_rent = models.FloatField(null=False)
    status = models.ForeignKey(Configurations, related_name="cnf_status", on_delete=models.CASCADE,null=False)
    deleted_at = models.DateTimeField(auto_now=False, auto_now_add=False,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    
    def __str__(self):
        return self.name
    
class InventoryHeader(models.Model):
    name = models.CharField(max_length=255,null=False,blank=False)
    code = models.CharField(max_length=255,null=False,blank=False)
    deleted_at = models.DateTimeField(auto_now=False, auto_now_add=False,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,  on_delete=models.CASCADE,null=False)
    
    def __str__(self):
        return self.name
    
class InventoryItems(models.Model):
    name = models.CharField(max_length=255,null=False,blank=False)
    code = models.CharField(max_length=255,null=False,blank=False)
    total_stock = models.IntegerField(default=0)
    used_stock = models.IntegerField(default=0)
    status = models.ForeignKey(Configurations, related_name="inv_status", on_delete=models.CASCADE,null=False) 
    inventory_header_id = models.ForeignKey(InventoryHeader, on_delete=models.CASCADE,null=False)
    deleted_at = models.DateTimeField(auto_now=False, auto_now_add=False,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
    
    def __str__(self):
        return self.name
    
class Bookings(models.Model):
    '''Manages room reservations / bookings'''
    room_id = models.ForeignKey(RoomDetails, related_name="room_id", on_delete=models.CASCADE,null=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    room_type_id = models.ForeignKey(RoomsHeader, on_delete=models.CASCADE,null=False)
    number_people = models.IntegerField(default = 1)
    check_in_date = models.DateTimeField(auto_now=False, auto_now_add=False,null=False)
    check_out_date = models.DateTimeField(auto_now=False, auto_now_add=False,null=True)
    expected_check_in_date = models.DateTimeField(auto_now=False, auto_now_add=False,null=True)
    days_in = models.IntegerField(default = 1)
    extras_items_id = models.CharField(max_length=255,null=False,blank=False)
    status = models.ForeignKey(Configurations, on_delete=models.CASCADE,null=False) 
    payment_method = models.ForeignKey(Configurations, related_name="cnf_payment_method", on_delete=models.CASCADE)
    checked_in_by = models.ForeignKey(User, related_name="check_user_id", on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user_id.first_name} {self.user_id.last_name}'
    
class Reviews(models.Model):
    '''Manages Consumer Feedbacks / reviews'''    
    consumer_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False)
    comment = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.consumer_id.first_name} {self.consumer_id.last_name}'
    
class InvoiceHeaders(models.Model):
    '''Manage Booking Invoice '''
    booking_id = models.ForeignKey(Bookings, related_name="booking_id", on_delete=models.CASCADE,null=False) 
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False) 
    checked_in_by = models.ForeignKey(User, related_name="chk_by_user_id", on_delete=models.CASCADE,null=True)
    total_amount = models.FloatField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    approved_by = models.ForeignKey(User, related_name="approved_by", on_delete=models.CASCADE,null=True)
    payment_method = models.ForeignKey(Configurations, related_name="inv_payment_method", on_delete=models.CASCADE)
    status = models.ForeignKey(Configurations, related_name="inv_hd_status", on_delete=models.CASCADE,null=False) 
    invoice_no = models.CharField( max_length=100,null=False)
    
    def __str__(self):
        return self.invoice_no
    
class InvoiceDetails(models.Model):
    '''Manage Booking Invoice '''
    invoice_header_id = models.ForeignKey(InvoiceHeaders, related_name="invoice_header_id", on_delete=models.CASCADE,null=False) 
    inventory_items_id = models.ForeignKey(InventoryItems, related_name="inventory_items_id", on_delete=models.CASCADE,null=False)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)    