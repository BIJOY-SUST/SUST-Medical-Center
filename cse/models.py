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

class MedicalInfo(models.Model):
    user = models.ForeignKey(CustomUser,default=1,on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctors,default=1,on_delete=models.CASCADE)

    history = models.TextField(null=False,blank=False,default=None)
    add_info = models.TextField(null=False,blank=False,default=None)
    test_advise = models.TextField(null=False,blank=False,default=None)
    adate = models.DateField(null=False,blank=False,default=None)
    age = models.IntegerField(null=False,blank=False,default=None)
    # docotr_email = models.EmailField(null=False,blank=False,default=None,max_length=100)

    medi_name_1 = models.CharField(null=False,blank=False,default=None,max_length=100)
    drug_limit_1 = models.CharField(null=False,blank=False,default=None,max_length=100)
    num_of_day_1 = models.CharField(null=False,blank=False,default=None,max_length=100)
    eat_time_1 = models.CharField(null=False,blank=False,default=None,max_length=100)

    medi_name_2 = models.CharField(null=False, blank=False, default=None, max_length=100)
    drug_limit_2 = models.CharField(null=False, blank=False, default=None, max_length=100)
    num_of_day_2 = models.CharField(null=False, blank=False, default=None, max_length=100)
    eat_time_2 = models.CharField(null=False, blank=False, default=None, max_length=100)

    medi_name_3 = models.CharField(null=False, blank=False, default=None, max_length=100)
    drug_limit_3 = models.CharField(null=False, blank=False, default=None, max_length=100)
    num_of_day_3 = models.CharField(null=False, blank=False, default=None, max_length=100)
    eat_time_3 = models.CharField(null=False, blank=False, default=None, max_length=100)

    medi_name_4 = models.CharField(null=False, blank=False, default=None, max_length=100)
    drug_limit_4 = models.CharField(null=False, blank=False, default=None, max_length=100)
    num_of_day_4 = models.CharField(null=False, blank=False, default=None, max_length=100)
    eat_time_4 = models.CharField(null=False, blank=False, default=None, max_length=100)

    medi_name_5 = models.CharField(null=False, blank=False, default=None, max_length=100)
    drug_limit_5 = models.CharField(null=False, blank=False, default=None, max_length=100)
    num_of_day_5 = models.CharField(null=False, blank=False, default=None, max_length=100)
    eat_time_5 = models.CharField(null=False, blank=False, default=None, max_length=100)

    medi_name_6 = models.CharField(null=False, blank=False, default=None, max_length=100)
    drug_limit_6 = models.CharField(null=False, blank=False, default=None, max_length=100)
    num_of_day_6 = models.CharField(null=False, blank=False, default=None, max_length=100)
    eat_time_6 = models.CharField(null=False, blank=False, default=None, max_length=100)

    medi_name_7 = models.CharField(null=False, blank=False, default=None, max_length=100)
    drug_limit_7 = models.CharField(null=False, blank=False, default=None, max_length=100)
    num_of_day_7 = models.CharField(null=False, blank=False, default=None, max_length=100)
    eat_time_7 = models.CharField(null=False, blank=False, default=None, max_length=100)

    medi_name_8 = models.CharField(null=False, blank=False, default=None, max_length=100)
    drug_limit_8 = models.CharField(null=False, blank=False, default=None, max_length=100)
    num_of_day_8 = models.CharField(null=False, blank=False, default=None, max_length=100)
    eat_time_8 = models.CharField(null=False, blank=False, default=None, max_length=100)

    medi_name_9 = models.CharField(null=False, blank=False, default=None, max_length=100)
    drug_limit_9 = models.CharField(null=False, blank=False, default=None, max_length=100)
    num_of_day_9 = models.CharField(null=False, blank=False, default=None, max_length=100)
    eat_time_9 = models.CharField(null=False, blank=False, default=None, max_length=100)

    medi_name_10 = models.CharField(null=False, blank=False, default=None, max_length=100)
    drug_limit_10 = models.CharField(null=False, blank=False, default=None, max_length=100)
    num_of_day_10 = models.CharField(null=False, blank=False, default=None, max_length=100)
    eat_time_10 = models.CharField(null=False, blank=False, default=None, max_length=100)



class MedicineInfo(models.Model):
    Medicine_id = models.AutoField(null=False,blank=False,default=None, primary_key=True)
    medicinename = models.CharField(null=False,blank=False,default=None,max_length=200)
    medicineRegno = models.CharField(null=False,blank=False,default=None,max_length=200 , unique=True)
    medicinebefore = models.IntegerField(null=False,blank=False,default=None)
    medicineafter = models.IntegerField(null=True,blank=True,default=None)
    medicinenow = models.IntegerField(null=False,blank=False,default=None)
