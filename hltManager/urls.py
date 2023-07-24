from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from .views.auth import login_user_data, logout_view
from .views import *
from .views.bookings import bookings_view
from .views.inventory import inventory
from hltManager import views




app_name = 'hotel'

urlpatterns = [
   path('',loadDashoardHome,name="loadDashoardHome"),
   path('rooms/',rooms, name='rooms'),
   path('bookings/', bookings_view, name='bookings'),
   path('inventory/',inventory, name='inventory'),
   path('login/', login_user_data, name='login'),
   path('logout/', logout_view, name='logout'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)