from django.shortcuts import render



def staring(request):
        return render(request, 'cse/staring.html')



def login(request):
        return render(request, 'cse/login.html')

def register(request):
        return render(request, 'cse/register.html')






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




