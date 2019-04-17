from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('cse.urls')),
    path('cse/',include('cse.urls',namespace='lol')),
]
