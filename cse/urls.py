from django.urls import path,re_path
from . import views
app_name = 'cse'

urlpatterns = [



    path('', views.staring, name='staring'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),

    path('index/', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('doctors/', views.doctors, name='doctors'),
    path('services/', views.services, name='services'),
    path('about_us/', views.about_us, name='about_us'),



    # path('blog_single/', views.blog_single, name='blog_single'),
    # path('departments_single/', views.departments_single, name='departments_single'),
    # path('doctors_single/', views.doctors_single, name='doctors_single'),
]