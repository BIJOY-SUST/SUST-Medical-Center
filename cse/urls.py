from django.urls import path,re_path
from cse import views as user_view
from django.conf import  settings
from django.contrib.auth import views as auth_views


app_name = 'cse'

urlpatterns = [

    path('test/',user_view.testing,name='test'),
    path('profile/',user_view.profile,name='profile'),
    path('profile_medi/',user_view.profile_medi,name='profile_medi'),
    path('per_medi_info/',user_view.per_medi_info,name='per_medi_info'),



    path('', user_view.staring, name='staring'),
    path('login/', user_view.login, name='login'),
    path('logout/', user_view.logout, name='logout'),
    path('register/', user_view.register, name='register'),

    path('password_reset/', user_view.password_reset, name='password_reset'),
    path('password_reset/done/', user_view.password_reset_done, name='password_reset_done'),
    path('password_reset/complete/', user_view.password_reset_complete, name='password_reset_complete'),


    path('index/', user_view.index, name='index'),
    path('contact/', user_view.contact, name='contact'),
    path('feedback/', user_view.feedback, name='feedback'),

    path('doctors/', user_view.doctors, name='doctors'),
    path('patient_to_doctor/', user_view.patient_to_doctor, name='patient_to_doctor'),
    path('<int:doctor_id>/doctors_delete/', user_view.doctors_delete, name='doctors_delete'),
    path('<int:doctor_id>/full_doctor/', user_view.full_doctor, name='full_doctor'),

    path('services/', user_view.services, name='services'),
    path('about_us/', user_view.about_us, name='about_us'),


    path('patientconfirm/', user_view.patientconfirm, name='patientconfirm'),
    path('pregform/', user_view.pregform, name='pregform'),
    # path('patientreg/',user_view.patient_reg,name='patient_reg'),
    # path('pdf/',user_view.GeneratePDF.as_view(),name='pdf'),
    path('pdf/',user_view.pdf,name='pdf'),


    path('newdoctor/', user_view.newdoctor, name='newdoctor'),
    path('newdoctor_reg/', user_view.newdoctorreg, name='newdoctor_reg'),



    # MedicineInfo
    path('medicineinfo/',user_view.medicineinfo,name='medicineinfo'),
    path('medisearch/',user_view.medisearch,name='medisearch'),
    path('medisearch2/',user_view.medisearch2,name='medisearch2'),
    path('newmedicine/',user_view.newmedicine,name='newmedicine'),
    path('mediregister/',user_view.mediregister,name='mediregister'),
    path('medi_pre/',user_view.medi_pre,name='medi_pre'),
    path('medichange/',user_view.medichange,name='medichange'),
    path('mediadd/',user_view.mediadd,name='mediadd'),

    # re_path(r'^medicineinfo/(?P<filter_by>[a-zA_Z]+)/$', user_view.medicineinfo,name='medicineinfo'),
    # re_path(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),


    # account confirmations
    # path('activate/<uid>/<token>/', views.activate,name='activate'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', user_view.activate, name='activate'),

    re_path(r'^passactivate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', user_view.passactivate, name='passactivate'),

]