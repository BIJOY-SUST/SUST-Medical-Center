from django.urls import path,re_path
from . import views
app_name = 'cse'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('appointment/', views.appointment, name='appointment'),
    path('blog/', views.blog, name='blog'),
    path('blog_single/', views.blog_single, name='blog_single'),
    path('contact/', views.contact, name='contact'),
    path('departments/', views.departments, name='departments'),
    path('departments_single/', views.departments_single, name='departments_single'),

    path('doctors_single/', views.doctors_single, name='doctors_single'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctors_single/', views.doctors_single, name='doctors_single'),
    path('services/', views.services, name='services'),





    path('', views.staring, name='staring'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),





]