import  json
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect,HttpResponse,NoReverseMatch,HttpResponsePermanentRedirect,Http404,HttpResponseRedirect
from django.db.models import Q
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import  settings
from django.core.mail import send_mail,EmailMessage
from django.contrib import  messages
from django.shortcuts import render
from datetime import date,datetime
from .models import CustomUser,Doctors

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def staring(request):
        return render(request, 'cse/staring.html')



def login(request):
        
        if request.method == "POST":
                email = request.POST['useremail']
                password = request.POST['password']

                # print(email)

                user = authenticate(email=email, password=password)
                if user is not None:
                        if user.is_active:
                                auth_login(request, user)
                                return render(request, 'cse/index.html')
                        else:
                                return render(request, 'cse/login.html',{'error_message': 'Your account has been disabled'})
                else:
                        return render(request, 'cse/login.html', {'error_message': 'Invalid login'})
        return render(request, 'cse/login.html')


def calculateAge(born):

        today = date.today()
        try:
                birthday = born.replace(year=today.year)

                # raised when birth date is February 29
        # and the current year is not a leap year
        except ValueError:
                birthday = born.replace(year=today.year,
                                        month=born.month + 1, day=1)

        if birthday > today:
                return today.year - born.year - 1
        else:
                return today.year - born.year


def register(request):
        if request.method=='POST':
                tfirstname = request.POST.get('firstname')
                tlastname = request.POST.get('lastname')
                tusername = request.POST.get('username')


                tbdate = request.POST.get('date_of_birth')

                tgender = request.POST.get('gender')
                taddress = request.POST.get('address')
                tmobileno = request.POST.get('mobileno')
                ttelno = request.POST.get('telno')
                tuseremail = request.POST.get('useremail')
                tusertype = request.POST.get('usertype')
                tregno = request.POST.get('regno')
                tdepartment = request.POST.get('department')
                tposition = request.POST.get('position')
                tbloodgroup = request.POST.get('bloodgroup')
                theight = request.POST.get('height')
                tpassword = request.POST.get('password')



                tnowdate = datetime.today()

                c = CustomUser(first_name=tfirstname,last_name=tlastname,username=tusername,date_of_birth=tbdate,gender=tgender,address=taddress,
                               mobile_no=tmobileno,tel_no=ttelno,email=tuseremail,user_type=tusertype,reg_no=tregno,department=tdepartment,
                               designation=tposition,blood_group=tbloodgroup,height=theight,is_superuser=False,date_joined=tnowdate,
                               is_staff=False,is_active=True,last_login=None)

                y = c.date_of_birth.month
                # m = c.date_of_birth.month
                # d = c.date_of_birth.day
                print(y)
                # tage = calculateAge(date(y,m,d))
                c.age = 20

                c.set_password(tpassword)
                c.photos = request.FILES['userphotos']
                file_type = c.photos.url.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:
                        context = {
                                'error_message': 'Image file must be PNG, JPG, or JPEG',
                        }
                        return render(request, 'cse/register.html', context)
                # tuserphotos = request.POST.get('userphotos')
                c.save()
                return render(request, 'cse/login.html')
        else:
                return render(request,'cse/register.html')





# User authentication er kahini ses akn theke baki kaj



def index(request):
        return render(request, 'cse/index.html')

def blog(request):
        return render(request, 'cse/blog.html')


def contact(request):
        return render(request, 'cse/contact.html')


def doctors(request):
        return render(request, 'cse/doctors.html')

def services(request):
        return render(request, 'cse/services.html')

def about_us(request):
        return render(request, 'cse/about_us.html')




