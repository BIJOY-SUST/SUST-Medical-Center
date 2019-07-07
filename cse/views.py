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
from .models import CustomUser,Doctors,FeebBack,MedicalInfo,MedicineInfo
from django.contrib import messages
from  django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from cse.utils import render_to_pdf
from django.shortcuts import get_object_or_404

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']



# ----------------- Testing ----------------------------

def testing(request):

    return render(request, 'cse/test3.html')
# ---------------------- Medical Info --------------------

def calculate_age(born):
    today = date.today()
    try:
        birthday = born.replace(year=today.year)
    except ValueError: # raised when birth date is February 29 and the current year is not a leap year
        birthday = born.replace(year=today.year, month=born.month+1, day=1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year


def per_medi_info(request):
    if not request.user.is_authenticated:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})
    else:
        if request.method == 'POST':
            t_patient = request.user
            t_doctor = Doctors.objects.get(doctor_id=request.POST.get('in_doc_id'))
            medi_in = MedicalInfo.objects.get(id=request.POST.get('in_mediingo_id'))
            context = {
                'tpatient': t_patient,
                'tdoctor': t_doctor,

                'thistory': medi_in.history,
                'tadditional_field': medi_in.add_info,
                'ttestadvised': medi_in.test_advise,

                'today_date': date.today(),
                'agee': medi_in.age,

                '1_medi_name': medi_in.medi_name_1,
                '1_drug_limit': medi_in.drug_limit_1,
                '1_days': medi_in.num_of_day_1,
                '1_eat': medi_in.eat_time_1,

                '2_medi_name': medi_in.medi_name_2,
                '2_drug_limit': medi_in.drug_limit_2,
                '2_days': medi_in.num_of_day_2,
                '2_eat': medi_in.eat_time_2,

                '3_medi_name': medi_in.medi_name_3,
                '3_drug_limit': medi_in.drug_limit_3,
                '3_days': medi_in.num_of_day_3,
                '3_eat': medi_in.eat_time_3,

                '4_medi_name': medi_in.medi_name_4,
                '4_drug_limit': medi_in.drug_limit_4,
                '4_days': medi_in.num_of_day_4,
                '4_eat': medi_in.eat_time_4,

                '5_medi_name': medi_in.medi_name_5,
                '5_drug_limit': medi_in.drug_limit_5,
                '5_days': medi_in.num_of_day_5,
                '5_eat': medi_in.eat_time_5,

                '6_medi_name': medi_in.medi_name_6,
                '6_drug_limit': medi_in.drug_limit_6,
                '6_days': medi_in.num_of_day_6,
                '6_eat': medi_in.eat_time_6,

                '7_medi_name': medi_in.medi_name_7,
                '7_drug_limit':medi_in.drug_limit_7,
                '7_days':medi_in.num_of_day_7,
                '7_eat': medi_in.eat_time_7,

                '8_medi_name': medi_in.medi_name_8,
                '8_drug_limit': medi_in.drug_limit_8,
                '8_days': medi_in.num_of_day_8,
                '8_eat': medi_in.eat_time_8,

                '9_medi_name': medi_in.medi_name_9,
                '9_drug_limit': medi_in.drug_limit_9,
                '9_days': medi_in.num_of_day_9,
                '9_eat': medi_in.eat_time_9,

                '10_medi_name': medi_in.medi_name_10,
                '10_drug_limit': medi_in.drug_limit_10,
                '10_days': medi_in.num_of_day_10,
                '10_eat': medi_in.eat_time_10
            }
            # html = template.render(context)
            # return HttpResponse(html)
            pdf = render_to_pdf('cse/prescription.html', context)

            # c = MedicalInfo(user_id=t_patient.id, prescription=pdf)
            # c.save()
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "Patient_%s.pdf" % ("Prescription")
                content = "inline; filename='%s'" % (filename)
                download = request.GET.get("download")
                if download:
                    content = "attachment; filename='%s'" % (filename)
                response['Content-Disposition'] = content
                return response
            else:
                return HttpResponse("Not found")

        else:
            userinfo = request.user
            medical = MedicalInfo.objects.filter(user_id=request.user.id)
            return render(request, 'cse/profile.html', {'userinfo': userinfo, 'medical': medical})


# ----------------------Login or Register with Logout--------------------

def logout(request):
    auth_logout(request)
    last_ten = FeebBack.objects.all().order_by('-id')[:10]
    return render(request, 'cse/staring.html', {'messages': last_ten})

def login(request):
        if request.method == 'POST':
                # temail = request.POST['useremail']
                # tpassword = request.POST['password']
                temail = request.POST.get('useremail')
                tpassword = request.POST.get('password')
                user = authenticate(email=temail, password=tpassword)
                if user is not None:
                        if user.is_active:
                                auth_login(request, user)
                                if request.user.is_superuser or user.user_type == 'Admin':
                                    last_ten = FeebBack.objects.all().order_by('-id')[:10]
                                    return render(request, 'cse/index_admin.html', {'messages': last_ten})
                                else:
                                    last_ten = FeebBack.objects.all().order_by('-id')[:10]
                                    return render(request, 'cse/index.html',{'messages': last_ten})

                        else:
                                messages.error(request, 'Your account has been disabled..!')
                                return render(request, 'cse/login.html')
                else:
                        messages.error(request, 'Invalid login..!')
                        return render(request, 'cse/login.html')
        else:
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
                    mail_subject = "Confirmation message for SUST Medical Center"
                    message = render_to_string('cse/confirm_email_admin.html', {
                            'user': c,
                            'domain': site,
                            # 'domain': get_current_site(request).domain,
                            'uid': urlsafe_base64_encode(force_bytes(c.pk)),
                            'token': account_activation_token.make_token(c),
                    })
                    from_email = settings.EMAIL_HOST_USER
                    to_email = settings.EMAIL_HOST_USER
                    to_list = [to_email]
                    send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
                    # emailcheck = EmailMessage(mail_subject, message, from_email, to_list,)
                    # emailcheck.send()
                    return render(request, 'cse/before_confirm_admin.html')
                else:
                    site = request.META['HTTP_HOST']
                    # print(site)
                    mail_subject = "Confirmation message for SUST Medical Center"
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
            return render(request, 'cse/register.html')

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


# ---------------------- Password Reset --------------------

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
                    mail_subject = "Confirmation message for SUST Medical Center"
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



# Start website - BIJOY_SUST

def profile(request):
    if not request.user.is_authenticated:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})

    else:
        userinfo= request.user
        medical = MedicalInfo.objects.filter(user_id=request.user.id)
        return render(request,'cse/profile.html',{'userinfo':userinfo,'medical':medical})

def profile_medi(request):
    if not request.user.is_authenticated:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})

    else:
        userinfo= request.user
        medical = MedicalInfo.objects.filter(user_id=request.user.id)
        return render(request,'cse/profile_medi.html',{'userinfo':userinfo,'medical':medical})



def staring(request):
    if not request.user.is_authenticated:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})
    elif request.user.is_superuser or request.user.user_type == 'Admin':
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/index_admin.html', {'messages': last_ten})
    else:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/index.html', {'messages': last_ten})


def index(request):
    if not request.user.is_authenticated:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})
    elif request.user.is_superuser or request.user.user_type == 'Admin':
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/index_admin.html', {'messages': last_ten})
    else:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/index.html', {'messages': last_ten})


def about_us(request):
    if not request.user.is_authenticated:
        return render(request,'cse/about_us_general.html')
    else:
        return render(request, 'cse/about_us.html')

def contact(request):
    if not request.user.is_authenticated:
        return render(request,'cse/contact_general.html')
    else:
        return render(request, 'cse/contact.html')

def feedback(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            sub  = request.POST.get('subject')
            mess  = request.POST.get('message')
            # adate = date.today()
            # print(adate)
            c=FeebBack(user_id=request.user.id,tsub=sub,tmessage=mess)
            c.save()
            mail_subject = "Thank you for your feedback"
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
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})

def doctors(request):
    if not request.user.is_authenticated:
        doctor = Doctors.objects.all()
        return render(request, 'cse/doctor_general.html',{'doctorlist':doctor})
    elif request.user.is_superuser:
        doctor = Doctors.objects.all()
        return render(request, 'cse/doctor_super.html',{'doctorlist':doctor})
    else:
        doctor = Doctors.objects.all()
        return render(request, 'cse/doctors.html',{'doctorlist':doctor})

def full_doctor(request,doctor_id):
    if not request.user.is_authenticated:
        doctor_s = Doctors.objects.get(pk=doctor_id)
        return render(request, 'cse/doctor_full_p_general.html',{'sin_doc':doctor_s})
    else:
        doctor_s = Doctors.objects.get(pk=doctor_id)
        return render(request, 'cse/doctor_full_profile.html',{'sin_doc':doctor_s})


def patient_to_doctor(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            sub = request.POST.get('subject')
            mess = request.POST.get('message')
            c = Doctors.objects.get(email=request.POST.get('in_email'))

            # System to doctor
            mail_subject = "Patient Request"
            message = render_to_string('cse/feed3.html', {
                'user': request.user,
                'doc' : c,
                'subj': sub,
                'messg': mess,
            })
            from_email = settings.EMAIL_HOST_USER
            to_email = c.email
            to_list = [to_email]
            send_mail(mail_subject, message, from_email, to_list, fail_silently=True)


            # system to patient
            mail_subject = "Thank you for your Email"
            message = render_to_string('cse/feed2.html', {
                'user': request.user,
            })
            from_email = settings.EMAIL_HOST_USER
            to_email = request.user.email
            to_list = [to_email]
            send_mail(mail_subject, message, from_email, to_list, fail_silently=True)

            return render(request, 'cse/doctor_full_profile.html', {'sin_doc':c})
        else:
            last_ten = FeebBack.objects.all().order_by('-id')[:10]
            return render(request, 'cse/staring.html', {'messages': last_ten})
    else:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})






def doctors_delete(request,doctor_id):
    if not request.user.is_authenticated:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})
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
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/services_general.html', {'messages': last_ten})



# Patient recorded created

def patientconfirm(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Admin' or request.user.is_superuser:
            return render(request, 'cse/patient_confirm.html')
        # elif request.user.is_superuser:
        #     return render(request,'cse/patient_confirm.html')
        else:
            last_ten = FeebBack.objects.all().order_by('-id')[:10]
            return render(request, 'cse/index.html', {'messages': last_ten})
    else:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})

def pregform(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Admin' or request.user.is_superuser:
            if request.method == 'POST':
                if CustomUser.objects.filter(email=request.POST.get('useremail')).exists():
                    c = CustomUser.objects.get(email=request.POST.get('useremail'))
                    if request.user.is_superuser or Doctors.objects.filter(email=request.user.email).exists():
                        c = CustomUser.objects.get(email=request.POST.get('useremail'))
                        if c.is_active == True:
                            doctor = Doctors.objects.all()

                            context = {
                                'user': c,
                                'doctorlist': doctor,
                                'sin_doc' : request.user
                            }

                            return render(request,'cse/pregform.html',context)
                        else:
                            messages.error(request, 'User email doesnot exists..!, Please enter a valid Email address.')
                            return render(request, 'cse/patient_confirm.html')

                    elif c.is_active:
                        messages.error(request, 'Yes, Valid Patient....!!!')
                        return render(request, 'cse/patient_confirm.html')
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
            last_ten = FeebBack.objects.all().order_by('-id')[:10]
            return render(request, 'cse/index.html', {'messages': last_ten})
    else:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})


# def patient_reg(request):
#     if request.user.is_authenticated:
#         if request.user.user_type == 'Admin' or request.user.is_superuser:
#             if request.method=='POST':
#                 t_patient = CustomUser.objects.get(email=request.POST.get('in_email'))
#                 t_doctor = Doctors.objects.get(email=request.POST.get('doctoremail'))
#                 context = {
#                     'tpatient' : t_patient,
#                     'tdoctor' : t_doctor,
#
#                     'thistory' : request.POST.get('history'),
#                     'tadditional_field' : request.POST.get('additional_field'),
#                     'ttestadvised' : request.POST.get('testadvised'),
#
#                     'today_date' : date.today(),
#
#
#                     '1_medi_name' : request.POST.get('medicine_1'),
#                     '1_drug_limit' : request.POST.get('drug_limit_1'),
#                     '1_eat' : request.POST.get('eating_time_1'),
#
#                     '2_medi_name': request.POST.get('medicine_2'),
#                     '2_drug_limit': request.POST.get('drug_limit_2'),
#                     '2_eat': request.POST.get('eating_time_2'),
#
#                     '3_medi_name': request.POST.get('medicine_3'),
#                     '3_drug_limit': request.POST.get('drug_limit_3'),
#                     '3_eat': request.POST.get('eating_time_3'),
#
#                     '4_medi_name': request.POST.get('medicine_4'),
#                     '4_drug_limit': request.POST.get('drug_limit_4'),
#                     '4_eat': request.POST.get('eating_time_4'),
#
#                     '5_medi_name': request.POST.get('medicine_5'),
#                     '5_drug_limit': request.POST.get('drug_limit_5'),
#                     '5_eat': request.POST.get('eating_time_5'),
#
#                     '6_medi_name': request.POST.get('medicine_6'),
#                     '6_drug_limit': request.POST.get('drug_limit_6'),
#                     '6_eat': request.POST.get('eating_time_6'),
#
#                     '7_medi_name': request.POST.get('medicine_7'),
#                     '7_drug_limit': request.POST.get('drug_limit_7'),
#                     '7_eat': request.POST.get('eating_time_7'),
#
#                     '8_medi_name': request.POST.get('medicine_8'),
#                     '8_drug_limit': request.POST.get('drug_limit_8'),
#                     '8_eat': request.POST.get('eating_time_8'),
#
#                     '9_medi_name': request.POST.get('medicine_9'),
#                     '9_drug_limit': request.POST.get('drug_limit_9'),
#                     '9_eat': request.POST.get('eating_time_9'),
#
#                     '10_medi_name': request.POST.get('medicine_10'),
#                     '10_drug_limit': request.POST.get('drug_limit_10'),
#                     '10_eat': request.POST.get('eating_time_10'),
#
#                 }
#                 return render(request,'cse/test.html',context)
#             else:
#                 # messages.error(request, 'Fill the form very carefully...!')
#                 return render(request,'cse/patient_confirm.html')
#         else:
#             return render(request,'cse/index.html')
#     else:
#         messages.error(request, 'Please login first...!')
#         return render(request, 'cse/login.html')

# class GeneratePDF(View):
#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             if request.user.user_type == 'Admin' or request.user.is_superuser:
#                 if request.method == 'POST' or request.method == 'GET':
#                 # if request.method == 'POST':
#                     # template = get_template('cse/test.html')
#
#
#                     t_patient = CustomUser.objects.get(email=request.POST.get('in_email'))
#                     t_doctor = Doctors.objects.get(email=request.POST.get('doctoremail'))
#                     context={
#                         'tpatient' : t_patient,
#                         'tdoctor' : t_doctor,
#
#                         'thistory' : request.POST.get('history'),
#                         'tadditional_field' : request.POST.get('additional_field'),
#                         'ttestadvised' : request.POST.get('testadvised'),
#
#                         'today_date' : date.today(),
#
#
#                         '1_medi_name' : request.POST.get('medicine_1'),
#                         '1_drug_limit' : request.POST.get('drug_limit_1'),
#                         '1_eat' : request.POST.get('eating_time_1'),
#
#                         '2_medi_name': request.POST.get('medicine_2'),
#                         '2_drug_limit': request.POST.get('drug_limit_2'),
#                         '2_eat': request.POST.get('eating_time_2'),
#
#                         '3_medi_name': request.POST.get('medicine_3'),
#                         '3_drug_limit': request.POST.get('drug_limit_3'),
#                         '3_eat': request.POST.get('eating_time_3'),
#
#                         '4_medi_name': request.POST.get('medicine_4'),
#                         '4_drug_limit': request.POST.get('drug_limit_4'),
#                         '4_eat': request.POST.get('eating_time_4'),
#
#                         '5_medi_name': request.POST.get('medicine_5'),
#                         '5_drug_limit': request.POST.get('drug_limit_5'),
#                         '5_eat': request.POST.get('eating_time_5'),
#
#                         '6_medi_name': request.POST.get('medicine_6'),
#                         '6_drug_limit': request.POST.get('drug_limit_6'),
#                         '6_eat': request.POST.get('eating_time_6'),
#
#                         '7_medi_name': request.POST.get('medicine_7'),
#                         '7_drug_limit': request.POST.get('drug_limit_7'),
#                         '7_eat': request.POST.get('eating_time_7'),
#
#                         '8_medi_name': request.POST.get('medicine_8'),
#                         '8_drug_limit': request.POST.get('drug_limit_8'),
#                         '8_eat': request.POST.get('eating_time_8'),
#
#                         '9_medi_name': request.POST.get('medicine_9'),
#                         '9_drug_limit': request.POST.get('drug_limit_9'),
#                         '9_eat': request.POST.get('eating_time_9'),
#
#                         '10_medi_name': request.POST.get('medicine_10'),
#                         '10_drug_limit': request.POST.get('drug_limit_10'),
#                         '10_eat': request.POST.get('eating_time_10'),
#                     }
#                     # html = template.render(context)
#                     # return HttpResponse(html)
#                     pdf = render_to_pdf('cse/prescription.html',context)
#                     if pdf:
#                         response = HttpResponse(pdf, content_type='application/pdf')
#                         filename = "Patient_%s.pdf" %("Prescription")
#                         content = "inline; filename='%s'" %(filename)
#                         download = request.GET.get("download")
#                         if download:
#                             content = "attachment; filename='%s'" %(filename)
#                         response['Content-Disposition'] = content
#                         return response
#                     return HttpResponse("Not found")
#                 else:
#                     # messages.error(request, 'Fill the form very carefully...!')
#                     return render(request, 'cse/patient_confirm.html')
#             else:
#                 return render(request, 'cse/index.html')
#         else:
#             messages.error(request, 'Please login first...!')
#             return render(request, 'cse/login.html')




def pdf(request):
    # bb = request.POST.get('history'),
    # print(bb)
    if request.user.is_authenticated:
        if request.user.user_type == 'Admin' or request.user.is_superuser:
            # if request.method == 'POST' or request.method == 'GET':
            if request.method == 'POST':
                # template = get_template('cse/test.html')
                # nam = request.user.first_name
                # print(nam)
                t_patient = CustomUser.objects.get(email=request.POST.get('in_email'))
                t_doctor = Doctors.objects.get(email=request.POST.get('doctoremail'))
                dd = t_patient.date_of_birth

                # medical_info Table

                # his = request.POST.get('history'),
                # addinfo = request.POST.get('additional_field'),
                # test = request.POST.get('testadvised'),

                # print(his)

                # a_date =  date.today(),
                # print(a_date)
                # one_name =  request.POST.get('medicine_1'),
                # one_limit= request.POST.get('drug_limit_1'),
                # one_day =  request.POST.get('days_1'),
                # one_eat =  request.POST.get('eating_time_1'),
                #
                # two_name =  request.POST.get('medicine_2'),
                # two_limit = request.POST.get('drug_limit_2'),
                # two_day = request.POST.get('days_2'),
                # two_eat =  request.POST.get('eating_time_2'),
                #
                # the_name =  request.POST.get('medicine_3'),
                # the_lim =  request.POST.get('drug_limit_3'),
                # the_da =  request.POST.get('days_3'),
                # the_eat = request.POST.get('eating_time_3'),
                #
                # f_name = request.POST.get('medicine_4'),
                # f_lim = request.POST.get('drug_limit_4'),
                # f_da = request.POST.get('days_4'),
                # f_eat = request.POST.get('eating_time_4'),
                #
                # fi_name = request.POST.get('medicine_5'),
                # fi_lim = request.POST.get('drug_limit_5'),
                # fi_day = request.POST.get('days_5'),
                # fi_eat = request.POST.get('eating_time_5'),
                #
                # si_name = request.POST.get('medicine_6'),
                # si_lim = request.POST.get('drug_limit_6'),
                # si_da = request.POST.get('days_6'),
                # si_eat = request.POST.get('eating_time_6'),
                #
                # se_name =  request.POST.get('medicine_7'),
                # se_lim= request.POST.get('drug_limit_7'),
                # se_da =  request.POST.get('days_7'),
                # se_eat = request.POST.get('eating_time_7'),
                #
                # ei_name= request.POST.get('medicine_8'),
                # ei_lim = request.POST.get('drug_limit_8'),
                # ei_day = request.POST.get('days_8'),
                # ei_eat = request.POST.get('eating_time_8'),
                #
                # ni_name = request.POST.get('medicine_9'),
                # ni_lim =  request.POST.get('drug_limit_9'),
                # ni_day =  request.POST.get('days_9'),
                # ni_eat = request.POST.get('eating_time_9'),
                #
                # ten_name =  request.POST.get('medicine_10'),
                # ten_lim= request.POST.get('drug_limit_10'),
                # ten_da= request.POST.get('days_10'),
                # ten_eat =  request.POST.get('eating_time_10'),

                c=MedicalInfo(user_id=t_patient.id,doctor_id=t_doctor.doctor_id, adate=date.today(),age=calculate_age(dd),
                              history=request.POST.get('history'),
                              add_info=request.POST.get('additional_field'),
                              test_advise=request.POST.get('testadvised'),

                              medi_name_1=request.POST.get('medicine_1'),
                              drug_limit_1=request.POST.get('drug_limit_1'),
                              num_of_day_1=request.POST.get('days_1'),
                              eat_time_1=request.POST.get('eating_time_1'),

                              medi_name_2=request.POST.get('medicine_2'),
                              drug_limit_2=request.POST.get('drug_limit_2'),
                              num_of_day_2=request.POST.get('days_2'),
                              eat_time_2=request.POST.get('eating_time_2'),

                              medi_name_3= request.POST.get('medicine_3'),
                              drug_limit_3=request.POST.get('drug_limit_3'),
                              num_of_day_3=request.POST.get('days_3'),
                              eat_time_3=request.POST.get('eating_time_3'),

                              medi_name_4=request.POST.get('medicine_4'),
                              drug_limit_4=request.POST.get('drug_limit_4'),
                              num_of_day_4=request.POST.get('days_4'),
                              eat_time_4= request.POST.get('eating_time_4'),


                              medi_name_5=request.POST.get('medicine_5'),
                              drug_limit_5=request.POST.get('drug_limit_5'),
                              num_of_day_5=request.POST.get('days_5'),
                              eat_time_5= request.POST.get('eating_time_5'),

                              medi_name_6= request.POST.get('medicine_6'),
                              drug_limit_6=request.POST.get('drug_limit_6'),
                              num_of_day_6=request.POST.get('days_6'),
                              eat_time_6=request.POST.get('eating_time_6'),

                              medi_name_7=request.POST.get('medicine_7'),
                              drug_limit_7=request.POST.get('drug_limit_7'),
                              num_of_day_7=request.POST.get('days_7'),
                              eat_time_7=request.POST.get('eating_time_7'),

                              medi_name_8=request.POST.get('medicine_8'),
                              drug_limit_8=request.POST.get('drug_limit_8'),
                              num_of_day_8=request.POST.get('days_8'),
                              eat_time_8=request.POST.get('eating_time_8'),

                              medi_name_9=request.POST.get('medicine_9'),
                              drug_limit_9=request.POST.get('drug_limit_9'),
                              num_of_day_9=request.POST.get('days_9'),
                              eat_time_9=request.POST.get('eating_time_9'),

                              medi_name_10=request.POST.get('medicine_10'),
                              drug_limit_10=request.POST.get('drug_limit_10'),
                              num_of_day_10=request.POST.get('days_10'),
                              eat_time_10=request.POST.get('eating_time_10')
                              )
                c.save()



                # End of medical_info Table


                context={
                    'tpatient' : t_patient,
                    'tdoctor' : t_doctor,

                    'thistory' : request.POST.get('history'),
                    'tadditional_field' : request.POST.get('additional_field'),
                    'ttestadvised' : request.POST.get('testadvised'),

                    'today_date' : date.today(),
                    'agee' : calculate_age(dd),

                    '1_medi_name' : request.POST.get('medicine_1'),
                    '1_drug_limit' : request.POST.get('drug_limit_1'),
                    '1_days' : request.POST.get('days_1'),
                    '1_eat' : request.POST.get('eating_time_1'),

                    '2_medi_name': request.POST.get('medicine_2'),
                    '2_drug_limit': request.POST.get('drug_limit_2'),
                    '2_days': request.POST.get('days_2'),
                    '2_eat': request.POST.get('eating_time_2'),

                    '3_medi_name': request.POST.get('medicine_3'),
                    '3_drug_limit': request.POST.get('drug_limit_3'),
                    '3_days': request.POST.get('days_3'),
                    '3_eat': request.POST.get('eating_time_3'),

                    '4_medi_name': request.POST.get('medicine_4'),
                    '4_drug_limit': request.POST.get('drug_limit_4'),
                    '4_days': request.POST.get('days_4'),
                    '4_eat': request.POST.get('eating_time_4'),

                    '5_medi_name': request.POST.get('medicine_5'),
                    '5_drug_limit': request.POST.get('drug_limit_5'),
                    '5_days': request.POST.get('days_5'),
                    '5_eat': request.POST.get('eating_time_5'),

                    '6_medi_name': request.POST.get('medicine_6'),
                    '6_drug_limit': request.POST.get('drug_limit_6'),
                    '6_days': request.POST.get('days_6'),
                    '6_eat': request.POST.get('eating_time_6'),

                    '7_medi_name': request.POST.get('medicine_7'),
                    '7_drug_limit': request.POST.get('drug_limit_7'),
                    '7_days': request.POST.get('days_7'),
                    '7_eat': request.POST.get('eating_time_7'),

                    '8_medi_name': request.POST.get('medicine_8'),
                    '8_drug_limit': request.POST.get('drug_limit_8'),
                    '8_days': request.POST.get('days_8'),
                    '8_eat': request.POST.get('eating_time_8'),

                    '9_medi_name': request.POST.get('medicine_9'),
                    '9_drug_limit': request.POST.get('drug_limit_9'),
                    '9_days': request.POST.get('days_9'),
                    '9_eat': request.POST.get('eating_time_9'),

                    '10_medi_name': request.POST.get('medicine_10'),
                    '10_drug_limit': request.POST.get('drug_limit_10'),
                    '10_days': request.POST.get('days_10'),
                    '10_eat': request.POST.get('eating_time_10'),
                }
                # html = template.render(context)
                # return HttpResponse(html)
                pdf = render_to_pdf('cse/prescription.html',context)

                # c = MedicalInfo(user_id=t_patient.id, prescription=pdf)
                # c.save()
                if pdf:
                    response = HttpResponse(pdf, content_type='application/pdf')
                    filename = "Patient_%s.pdf" %("Prescription")
                    content = "inline; filename='%s'" %(filename)
                    download = request.GET.get("download")
                    if download:
                        content = "attachment; filename='%s'" %(filename)
                    response['Content-Disposition'] = content
                    return response
                else:
                    return HttpResponse("Not found")
            else:
                # messages.error(request, 'Fill the form very carefully...!')
                return render(request, 'cse/patient_confirm.html')
        else:
            last_ten = FeebBack.objects.all().order_by('-id')[:10]
            return render(request, 'cse/index.html', {'messages': last_ten})
    else:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})











# Doctor recorded created

def newdoctor(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request,'cse/doctorreg.html')
        else:
            last_ten = FeebBack.objects.all().order_by('-id')[:10]
            return render(request, 'cse/index.html', {'messages': last_ten})
    else:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})
def newdoctorreg(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
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
                # messages.error(request, 'Error..!')
                return render(request,'cse/doctorreg.html')
        else:
            last_ten = FeebBack.objects.all().order_by('-id')[:10]
            return render(request, 'cse/index.html', {'messages': last_ten})
    else:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})



# Medicine er kaj suru

def medicineinfo(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Admin' or request.user.is_superuser:
            context={
                'medicineall' : MedicineInfo.objects.all(),
            }
            return render(request,'cse/medicineall.html',context)
        else:
            last_ten = FeebBack.objects.all().order_by('-id')[:10]
            return render(request, 'cse/index.html', {'messages': last_ten})
    else:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})

def medi_pre(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Admin' or request.user.is_superuser:
            context={
                'medicineall' : MedicineInfo.objects.all(),
            }
            return render(request,'cse/medi_pre.html',context)
        else:
            last_ten = FeebBack.objects.all().order_by('-id')[:10]
            return render(request, 'cse/index.html', {'messages': last_ten})
    else:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})



def medisearch(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Admin' or request.user.is_superuser:
            mediall = MedicineInfo.objects.all()
            query = request.GET.get("q")
            if query:
                medi_results = mediall.filter(
                    Q(medicinename__icontains=query)|
                    Q(medicineRegno__icontains=query)
                    ).distinct()
                context = {
                    'medicineall': medi_results,
                }
                return render(request, 'cse/medicineall.html', context)
            else:
                return render(request,'cse/medicineall.html')

        else:
            last_ten = FeebBack.objects.all().order_by('-id')[:10]
            return render(request, 'cse/index.html', {'messages': last_ten})
    else:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})

def medisearch2(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Admin' or request.user.is_superuser:
            mediall = MedicineInfo.objects.all()
            query = request.GET.get("q")
            if query:
                medi_results = mediall.filter(
                    Q(medicinename__icontains=query)|
                    Q(medicineRegno__icontains=query)
                    ).distinct()
                context = {
                    'medicineall': medi_results,
                }
                return render(request, 'cse/medi_pre.html', context)
            else:
                return render(request,'cse/medi_pre.html')

        else:
            last_ten = FeebBack.objects.all().order_by('-id')[:10]
            return render(request, 'cse/index.html', {'messages': last_ten})
    else:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})





def newmedicine(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Admin' or request.user.is_superuser:
            return render(request,'cse/medicinenew.html')
        else:
            last_ten = FeebBack.objects.all().order_by('-id')[:10]
            return render(request, 'cse/index.html', {'messages': last_ten})
    else:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})



def mediregister(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Admin' or request.user.is_superuser:
            if request.method=='POST':

                tname = request.POST.get('mediname')
                # print(tname)
                tregno = request.POST.get('medireg')
                tquantity = request.POST.get('medicnt')

                c = MedicineInfo(medicinename=tname,medicineRegno=tregno,medicinebefore=tquantity,medicineafter=0,medicinenow=tquantity)
                c.save()
                context = {
                    'medicineall': MedicineInfo.objects.all(),
                }
                return render(request, 'cse/medicineall.html', context)
            else:
                return render(request,'cse/medicinenew.html')
        else:
            last_ten = FeebBack.objects.all().order_by('-id')[:10]
            return render(request, 'cse/index.html', {'messages': last_ten})
    else:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})




def medichange(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Admin' or request.user.is_superuser:
            if request.method=='POST':

                tid = request.POST.get('in_id')
                tval = request.POST.get('medicnt')
                t_medi = MedicineInfo.objects.get(Medicine_id=tid)
                # print(t_medi.medicinebefore)
                # print(t_medi.medicineafter)
                # print(t_medi.medicinenow)
                # print(tval)
                tt = int(tval,10)
                # tt = tval
                t_medi.medicineafter = t_medi.medicineafter + tt
                t_medi.medicinenow = t_medi.medicinenow - tt
                t_medi.save()

                context = {
                    'medicineall': MedicineInfo.objects.all(),
                }
                return render(request, 'cse/medicineall.html', context)
            else:
                return render(request,'cse/medicineall.html')
        else:
            last_ten = FeebBack.objects.all().order_by('-id')[:10]
            return render(request, 'cse/index.html', {'messages': last_ten})
    else:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})


def mediadd(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'Admin' or request.user.is_superuser:
            if request.method=='POST':

                tid = request.POST.get('in_id2')
                tval = request.POST.get('medicnt2')
                t_medi = MedicineInfo.objects.get(Medicine_id=tid)
                # print(t_medi.medicinebefore)
                # print(t_medi.medicineafter)
                # print(t_medi.medicinenow)
                # print(tval)
                tt = int(tval,10)
                # tt = tval
                t_medi.medicinebefore = t_medi.medicinebefore + tt
                t_medi.medicinenow = t_medi.medicinenow + tt

                t_medi.save()

                context = {
                    'medicineall': MedicineInfo.objects.all(),
                }
                return render(request, 'cse/medi_pre.html', context)
            else:
                return render(request,'cse/medi_pre.html')
        else:
            last_ten = FeebBack.objects.all().order_by('-id')[:10]
            return render(request, 'cse/index.html', {'messages': last_ten})
    else:
        last_ten = FeebBack.objects.all().order_by('-id')[:10]
        return render(request, 'cse/staring.html', {'messages': last_ten})

