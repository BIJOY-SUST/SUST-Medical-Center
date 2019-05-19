from django.urls import path,re_path
from cse import views as user_view
from django.conf import  settings
from django.contrib.auth import views as auth_views


app_name = 'cse'

urlpatterns = [



    path('', user_view.staring, name='staring'),
    path('login/', user_view.login, name='login'),
    path('logout/', user_view.logout, name='logout'),
    path('register/', user_view.register, name='register'),

    path('password_reset/', user_view.password_reset, name='password_reset'),
    path('password_reset/done/', user_view.password_reset_done, name='password_reset_done'),
    path('password_reset/complete/', user_view.password_reset_complete, name='password_reset_complete'),


    path('index/', user_view.index, name='index'),
    path('blog/', user_view.blog, name='blog'),
    path('contact/', user_view.contact, name='contact'),
    path('doctors/', user_view.doctors, name='doctors'),
    path('services/', user_view.services, name='services'),
    path('about_us/', user_view.about_us, name='about_us'),

    # account confirmations
    # path('activate/<uid>/<token>/', views.activate,name='activate'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', user_view.activate, name='activate'),

    re_path(r'^passactivate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', user_view.passactivate, name='passactivate'),

]