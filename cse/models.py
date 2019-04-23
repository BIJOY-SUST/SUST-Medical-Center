
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # add additional fields in here
    # Contact = models.CharField(max_length=20)
    # date_of_birth = models.DateField()
    height = models.FloatField(null=False,blank=True,default=None)
    date_of_birth = models.DateField(null=False,blank=True,default=None)
    # gender = models.Con

    def __str__(self):

        return self.email