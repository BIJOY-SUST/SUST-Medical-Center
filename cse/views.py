import  json
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User,AbstractUser
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect,HttpResponse,NoReverseMatch,HttpResponsePermanentRedirect,Http404,HttpResponseRedirect
from django.db.models import Q
from .token import account_activation_token
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
from django.contrib import messages
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def staring(request):
        return render(request, 'cse/staring.html')

def login(request):
        if request.method == "POST":
                temail = request.POST['useremail']
                tpassword = request.POST['password']
                user = authenticate(email=temail, password=tpassword)
                if user is not None:
                        if user.is_active:
                                auth_login(request, user,backend='allauth.account.auth_backends.AuthenticationBackend')
                                return render(request, 'cse/index.html')
                        else:
                                messages.error(request, 'Your account has been disabled..!')
                                return render(request, 'cse/login.html')
                else:
                        messages.error(request, 'Invalid login..!')
                        return render(request, 'cse/login.html')
        return render(request, 'cse/login.html')


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
                               is_staff=False,last_login=None)


                c.set_password(tpassword)
                c.photos = request.FILES['userphotos']
                file_type = c.photos.url.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:
                        messages.error(request, 'Image file must be PNG, JPG, or JPEG')
                        return render(request, 'cse/register.html')

                if CustomUser.objects.filter(username=request.POST.get('username')).exists():
                        messages.error(request, 'User name is already exists..!')
                        return render(request, 'cse/register.html')

                if CustomUser.objects.filter(email=request.POST.get('useremail')).exists():
                        messages.error(request, 'User email is already exists..!')
                        return render(request, 'cse/register.html')

                c.is_active=False
                c.save()

                site = get_current_site(request)
                mail_subject = "Confirmation message for SUSTMedicalCenter"
                message = render_to_string('cse/confirm_email.html', {
                        'user': c,
                        'domain': site.domain,
                        # 'uid' : c.id,
                        'uid': urlsafe_base64_encode(force_bytes(c.pk)),
                        'token': account_activation_token.make_token(c),
                })
                from_email = settings.EMAIL_HOST_USER
                to_email = c.email
                to_list = [to_email]
                send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
                return render(request, 'cse/before_confirm.html')
        else:
                return render(request,'cse/register.html')


def activate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
        # return redirect('home')
        return render(request,'cse/after_confirm.html')
    else:
        return HttpResponse("<h2>Activation link is invalid...! <a href='/register'> Return</a>  to the register page.</h2>")
























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




