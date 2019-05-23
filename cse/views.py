import  json
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User,AbstractUser
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect,HttpResponse,NoReverseMatch,HttpResponsePermanentRedirect,Http404,HttpResponseRedirect
from django.db.models import Q
from .token import account_activation_token
from .token_admin import account_activation_token_admin
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.conf import  settings
from django.core.mail import send_mail,EmailMessage
from django.contrib import  messages
from django.shortcuts import render
from datetime import date,datetime
from .models import CustomUser,Doctors,FeebBack
from django.contrib import messages
from django.shortcuts import get_object_or_404

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def testing(request):
    return render(request,'cse/test.html')

def staring(request):
        # site = get_current_site(request).dom
        #
        #
        #
        # ain,
        # site = request.META['HTTP_HOST']
        # print(site)
        return render(request, 'cse/staring.html')

def logout(request):
    auth_logout(request)
    return render(request, 'cse/staring.html')

def login(request):
        if request.method == 'POST':
                # temail = request.POST['useremail']
                # tpassword = request.POST['password']

                temail = request.POST.get('useremail')
                tpassword = request.POST.get('password')

                user = authenticate(email=temail, password=tpassword)
                if user is not None:
                        if user.is_active:
                                # user.user_type='Admin'
                                # user.save()
                                auth_login(request, user)
                                if request.user.is_superuser:
                                    last_ten = FeebBack.objects.all().order_by('-id')[:10]
                                    doctor = Doctors.objects.all()
                                    return render(request, 'cse/indexsuper.html',{'messages': last_ten, 'doctorlist': doctor})

                                elif user.user_type == 'Admin':
                                    last_ten = FeebBack.objects.all().order_by('-id')[:10]
                                    doctor = Doctors.objects.all()
                                    return render(request, 'cse/index_admin.html',{'messages': last_ten, 'doctorlist': doctor})
                                else:
                                    last_ten = FeebBack.objects.all().order_by('-id')[:10]
                                    doctor = Doctors.objects.all()
                                    return render(request, 'cse/index.html',{'messages': last_ten, 'doctorlist': doctor})

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
                tpassword = request.POST.get('psw')
                tnowdate = datetime.today()
                tpas_reset = 0

                c = CustomUser(first_name=tfirstname,last_name=tlastname,username=tusername,date_of_birth=tbdate,gender=tgender,address=taddress,
                               mobile_no=tmobileno,tel_no=ttelno,email=tuseremail,user_type=tusertype,reg_no=tregno,department=tdepartment,
                               designation=tposition,blood_group=tbloodgroup,height=theight,is_superuser=False,date_joined=tnowdate,
                               is_staff=False,last_login=None,pass_reset=tpas_reset)


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

                if c.user_type == 'Admin':
                    site = request.META['HTTP_HOST']
                    # print(site)
                    mail_subject = "Confirmation message for SUSTMedicalCenter"
                    message = render_to_string('cse/confirm_email_admin.html', {
                            'user': c,
                            'domain': site,
                            # 'domain': get_current_site(request).domain,
                            'uid': urlsafe_base64_encode(force_bytes(c.pk)),
                            'token': account_activation_token.make_token(c),
                    })
                    from_email = settings.EMAIL_HOST_USER
                    to_email = 'bsbijoy2050@gmail.com'
                    to_list = [to_email]
                    send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
                    # emailcheck = EmailMessage(mail_subject, message, from_email, to_list,)
                    # emailcheck.send()
                    return render(request, 'cse/before_confirm_admin.html')
                else:
                    site = request.META['HTTP_HOST']
                    # print(site)
                    mail_subject = "Confirmation message for SUSTMedicalCenter"
                    message = render_to_string('cse/confirm_email.html', {
                            'user': c,
                            'domain': site,
                            # 'domain': get_current_site(request).domain,
                            'uid': urlsafe_base64_encode(force_bytes(c.pk)),
                            'token': account_activation_token.make_token(c),
                    })
                    from_email = settings.EMAIL_HOST_USER
                    to_email = request.POST.get('useremail')
                    to_list = [to_email]
                    send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
                    # emailcheck = EmailMessage(mail_subject, message, from_email, to_list,)
                    # emailcheck.send()
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
        # auth_login(request, user)
        if user.user_type == 'Admin':
            return render(request,'cse/after_confirm_admin.html')
        else:
            return render(request,'cse/after_confirm.html')
    else:
        return render(request,'cse/if_invalid.html')








# ----------------------Password Reset er kaj sguru--------------------


def password_reset(request):
        return render(request,'cse/password_reset.html')

def password_reset_done(request):
        if request.method=='POST':
            if CustomUser.objects.filter(email=request.POST.get('useremail')).exists():
                c = CustomUser.objects.get(email=request.POST.get('useremail'))
                if c.is_active == True:
                    c.pass_reset=True
                    c.save()
                    site = request.META['HTTP_HOST']
                    # print(site)
                    mail_subject = "Confirmation message for SUSTMedicalCenter"
                    message = render_to_string('cse/confirm_email_pass.html', {
                            'user': c,
                            'domain': site,
                            # 'domain': get_current_site(request).domain,
                            'uid': urlsafe_base64_encode(force_bytes(c.pk)),
                            'token': account_activation_token.make_token(c),
                    })
                    from_email = settings.EMAIL_HOST_USER
                    to_email = request.POST.get('useremail')
                    to_list = [to_email]
                    send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
                    return render(request,'cse/password_reset_done.html')
                else:
                    messages.error(request, 'User email doesnot exists..!, Please enter a valid Email address.')
                    return render(request, 'cse/password_reset.html')
            else:
                messages.error(request, 'User email doesnot exists..!, Please enter a valid Email address.')
                return render(request, 'cse/password_reset.html')
        else:
            return render(request, 'cse/password_reset.html')



def passactivate(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token_admin.check_token(user, token):
        if user.pass_reset:
            user.pass_reset=False
            user.save()
            return render(request,'cse/after_confirm_pass.html', {'user':user})
        else:
            render(request,'cse/if_invalid_pass.html')

    else:
        return render(request,'cse/if_invalid_pass.html')


def password_reset_complete(request):
    if request.method == 'POST':
        if CustomUser.objects.filter(email=request.POST.get('in_email')).exists():
            # tt = request.POST.get('in_email')
            # print(tt)
            c = CustomUser.objects.get(email=request.POST.get('in_email'))
            tpass = request.POST.get('psw')
            c.set_password(tpass)
            c.save()
            return render(request,'cse/password_reset_confirm.html')
        else:
            return render(request,'cse/password_reset.html')
    else:
        messages.error(request, 'Failed....!')
        return render(request,'cse/password_reset.html')

# def reset(request):
#         return render(request,'cse/password_reset_done.html')



















# User authentication er kahini ses akn theke baki kaj

def index(request):
    if not request.user.is_authenticated:
        return render(request,'cse/login.html')
    elif request.user.is_superuser:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        doctor = Doctors.objects.all()
        return render(request, 'cse/indexsuper.html', {'messages': last_ten,'doctorlist':doctor})
    elif request.user.user_type == 'Admin':
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        doctor = Doctors.objects.all()
        return render(request, 'cse/index_admin.html', {'messages': last_ten,'doctorlist':doctor})
    else:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        doctor = Doctors.objects.all()
        return render(request, 'cse/index.html', {'messages': last_ten,'doctorlist':doctor})

def blog(request):
    if not request.user.is_authenticated:
        return render(request, 'cse/login.html')
    else:
        return render(request, 'cse/blog.html')
def contact(request):
    if not request.user.is_authenticated:
        return render(request,'cse/login.html')
    else:
        return render(request, 'cse/contact.html')

def feedback(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            sub  = request.POST.get('subject')
            mess  = request.POST.get('message')
            c=FeebBack(user_id=request.user.id,tsub=sub,tmessage=mess)
            c.save()
            mail_subject = "Thankyou for your feedback"
            message = render_to_string('cse/feed.html', {
                'user': request.user,
            })
            from_email = settings.EMAIL_HOST_USER
            to_email = request.user.email
            to_list = [to_email]
            send_mail(mail_subject, message, from_email, to_list, fail_silently=True)

            return render(request,'cse/contact.html')
        else:
            return render(request,'cse/contact.html')
    else:
        return render(request,'cse/login.html')

def doctors(request):
    if not request.user.is_authenticated:
        return render(request, 'cse/login.html')
    elif request.user.is_superuser:
        doctor = Doctors.objects.all()
        return render(request, 'cse/doctor_super.html',{'doctorlist':doctor})
    else:
        doctor = Doctors.objects.all()
        return render(request, 'cse/doctors.html',{'doctorlist':doctor})



def doctors_delete(request,doctor_id):
    if not request.user.is_authenticated:
        return render(request, 'cse/login.html')
    elif request.user.is_superuser:
        doctor_s = Doctors.objects.get(pk=doctor_id)
        doctor_s.delete()
        doctor = Doctors.objects.all()
        return render(request, 'cse/doctor_super.html',{'doctorlist':doctor})
    else:
        doctor = Doctors.objects.all()
        return render(request, 'cse/doctors.html',{'doctorlist':doctor})




def services(request):
    if request.user.is_authenticated:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/services.html',{'messages': last_ten})
    else:
        return render(request,'cse/login.html')

def about_us(request):
    if not request.user.is_authenticated:
        return render(request, 'cse/login.html')
    else:
        return render(request, 'cse/about_us.html')





# Patient recorded created

def patientconfirm(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Admin':
            return render(request, 'cse/patient_confirm.html')
        elif request.user.is_superuser:
            return render(request,'cse/patient_confirm.html')
        else:
            return render(request,'cse/index.html')
    else:
        return render(request,'cse/login.html')

def pregform(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Admin' or request.user.is_superuser:
            if request.method == 'POST':
                if CustomUser.objects.filter(email=request.POST.get('useremail')).exists():
                    c = CustomUser.objects.get(email=request.POST.get('useremail'))
                    if c.is_active == True:
                        doctor = Doctors.objects.all()
                        return render(request,'cse/pregform.html',{'user':c,'doctorlist':doctor})
                    else:
                        messages.error(request, 'User email doesnot exists..!, Please enter a valid Email address.')
                        return render(request, 'cse/patient_confirm.html')
                else:
                    messages.error(request, 'User email doesnot exists..!, Please enter a valid Email address.')
                    return render(request, 'cse/patient_confirm.html')
            else:
                # messages.error(request, 'After entering patient email , please click the PROCEED button.')
                return render(request,'cse/patient_confirm.html')
        else:
            return render(request,'cse/index.html')
    else:
        messages.error(request, 'Please login first...!')
        return render(request, 'cse/login.html')


def patient_reg(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Admin' or request.user.is_superuser:
            if request.method=='POST':
                t_patient = CustomUser.objects.get(email=request.POST.get('in_email'))
                t_doctor = Doctors.objects.get(email=request.POST.get('doctoremail'))
                context = {
                    'tpatient' : t_patient,
                    'tdoctor' : t_doctor,

                    'thistory' : request.POST.get('history'),
                    'tadditional_field' : request.POST.get('additional_field'),
                    'ttestadvised' : request.POST.get('testadvised'),

                    'today_date' : date.today(),


                    '1_medi_name' : request.POST.get('medicine_1'),
                    '1_drug_limit' : request.POST.get('drug_limit_1'),
                    '1_eat' : request.POST.get('eating_time_1'),

                    '2_medi_name': request.POST.get('medicine_2'),
                    '2_drug_limit': request.POST.get('drug_limit_2'),
                    '2_eat': request.POST.get('eating_time_2'),

                    '3_medi_name': request.POST.get('medicine_3'),
                    '3_drug_limit': request.POST.get('drug_limit_3'),
                    '3_eat': request.POST.get('eating_time_3'),

                    '4_medi_name': request.POST.get('medicine_4'),
                    '4_drug_limit': request.POST.get('drug_limit_4'),
                    '4_eat': request.POST.get('eating_time_4'),

                    '5_medi_name': request.POST.get('medicine_5'),
                    '5_drug_limit': request.POST.get('drug_limit_5'),
                    '5_eat': request.POST.get('eating_time_5'),

                    '6_medi_name': request.POST.get('medicine_6'),
                    '6_drug_limit': request.POST.get('drug_limit_6'),
                    '6_eat': request.POST.get('eating_time_6'),

                    '7_medi_name': request.POST.get('medicine_7'),
                    '7_drug_limit': request.POST.get('drug_limit_7'),
                    '7_eat': request.POST.get('eating_time_7'),

                    '8_medi_name': request.POST.get('medicine_8'),
                    '8_drug_limit': request.POST.get('drug_limit_8'),
                    '8_eat': request.POST.get('eating_time_8'),

                    '9_medi_name': request.POST.get('medicine_9'),
                    '9_drug_limit': request.POST.get('drug_limit_9'),
                    '9_eat': request.POST.get('eating_time_9'),

                    '10_medi_name': request.POST.get('medicine_10'),
                    '10_drug_limit': request.POST.get('drug_limit_10'),
                    '10_eat': request.POST.get('eating_time_10'),

                }
                return render(request,'cse/prescription.html',context)
            else:
                # messages.error(request, 'Fill the form very carefully...!')
                return render(request,'cse/patient_confirm.html')
        else:
            return render(request,'cse/index.html')
    else:
        messages.error(request, 'Please login first...!')
        return render(request, 'cse/login.html')






# Doctor recorded created

def newdoctor(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request,'cse/doctorreg.html')
        else:
            return render(request,'cse/staring.html')
    else:
        return render(request,'cse/login.html')

def newdoctorreg(request):
    if request.user.is_authenticated:
        if request.method=='POST':
                tfirstname = request.POST.get('firstname')
                tlastname = request.POST.get('lastname')
                tgender = request.POST.get('gender')
                taddress = request.POST.get('address')
                tqualifications = request.POST.get('qualifications')
                tmobileno = request.POST.get('mobileno')
                ttelno = request.POST.get('telno')
                tuseremail = request.POST.get('useremail')
                tposition = request.POST.get('position')
                c = Doctors(first_name=tfirstname,last_name=tlastname,positions=tposition,gender=tgender,address=taddress,qualification=tqualifications,
                               mobile_no=tmobileno,tel_no=ttelno,email=tuseremail)

                c.doctorphoto = request.FILES['userphotos']
                file_type = c.doctorphoto.url.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:
                        messages.error(request, 'Image file must be PNG, JPG, or JPEG')
                        return render(request, 'cse/doctorreg.html')


                if Doctors.objects.filter(email=request.POST.get('useremail')).exists():
                        messages.error(request, 'User email is already exists..!')
                        return render(request, 'cse/doctorreg.html')

                c.save()
                messages.error(request, 'Doctors record created successfully..!')
                return render(request, 'cse/doctorreg.html')
        else:
            messages.error(request, 'Error..!')
            return render(request,'cse/doctorreg.html')

    else:
        return render(request,'cse/login.html')