from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from . import views
from .views import *



app_name = 'hotel'
urlpatterns = [
   path('',loadDashoardHome,name="loadDashoardHome"),
   path('/bookings',views.bookings,name="bookings")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)