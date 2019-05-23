from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    height = models.FloatField(null=False,blank=False,default=None)
    date_of_birth = models.DateField(null=False,blank=False,default=None)
    reg_no = models.CharField(null=True,blank=True,default=None,max_length=20)
    address = models.TextField(null=False,blank=False,default=None)
    gender = models.CharField(null=False,blank=False,default=None,max_length=20)
    user_type = models.CharField(null=False,blank=False,default=None,max_length=20)
    mobile_no = models.CharField(null=False,blank=False,default=None,max_length=20)
    tel_no = models.CharField(null=False,blank=False,default=None,max_length=20)
    # age = models.CharField(null=False,blank=False,default=None,max_length=90)
    department = models.CharField(null=True,blank=True,default=None,max_length=90)
    designation = models.CharField(null=True,blank=True,default=None,max_length=90)
    blood_group = models.CharField(null=False,blank=False,default=None,max_length=20)
    photos = models.FileField(null=False,blank=False,default=None,upload_to='images/')
    pass_reset = models.BooleanField(null=False,blank=False,default=None)



    def __str__(self):
        return self.email


class Doctors(models.Model):
    doctor_id = models.AutoField(null=False,blank=False,default=None, primary_key=True)
    email = models.EmailField(null=False,blank=False,default=None,unique=True)
    first_name = models.CharField(null=False,blank=False,default=None,max_length=40)
    last_name = models.CharField(null=False,blank=False,default=None,max_length=40)
    gender = models.CharField(null=False,blank=False,default=None,max_length=20)
    address = models.TextField(null=False, blank=False, default=None)
    mobile_no = models.CharField(null=False,blank=False,default=None,max_length=20)
    tel_no = models.CharField(null=False,blank=False,default=None,max_length=20)
    qualification = models.TextField(null=False,blank=False,default=None)
    doctorphoto = models.FileField(null=False,blank=False,default=None,upload_to='doctor/')
    positions = models.CharField(null=False,blank=False,default=None,max_length=100)
    # available_time_start = models.TimeField(null=False,blank=False,default=None)
    # available_time_end = models.TimeField(null=False,blank=False,default=None)



    def __str__(self):
        return self.email

class FeebBack(models.Model):
    user = models.ForeignKey(CustomUser,default=1,on_delete=models.CASCADE)
    tsub = models.CharField(null=False,blank=False,default=None,max_length=100)
    tmessage = models.TextField(null=False,blank=False,default=None)
    # pic = models.FileField(null=False,blank=False,default=None,upload_to='feed/')

    def __str__(self):
        return self.user.email