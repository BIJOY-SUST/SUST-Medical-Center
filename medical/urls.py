from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('cse.urls')),

    path('accounts/', include('allauth.urls')),  # new
    path('cse/',include('cse.urls',namespace='lol')),
]


if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)