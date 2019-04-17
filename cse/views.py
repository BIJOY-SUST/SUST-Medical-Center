from django.shortcuts import render



def appointment(request):
        return render(request, 'cse/appointment.html')

def blog(request):
        return render(request, 'cse/blog.html')

def blog_single(request):
        return render(request, 'cse/blog-single.html')

def contact(request):
        return render(request, 'cse/contact.html')

def departments(request):
        return render(request, 'cse/departments.html')

def departments_single(request):
        return render(request, 'cse/departments-single.html')

def doctors(request):
        return render(request, 'cse/doctors.html')

def doctors_single(request):
        return render(request, 'cse/doctors-single.html')

def index(request):
        return render(request, 'cse/index.html')

def services(request):
        return render(request, 'cse/services.html')


def staring(request):
        return render(request, 'cse/staring.html')

def login(request):
        return render(request, 'cse/login.html')

def register(request):
        return render(request, 'cse/register.html')

