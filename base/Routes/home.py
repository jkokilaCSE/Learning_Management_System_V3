from django.shortcuts import render, redirect
from .Tool.blogTool import get_images
from base.models import Teacher
from django.contrib.auth.models import User

# from django.core.mail import send_mail
# from django.conf import settings
# import smtplib
# import ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart


def pre_home(request):
    item = get_images()
    if request.user.is_authenticated:
        try:
            Teacher.objects.get(user=User.objects.get(id=request.user.id))
            return redirect('staff_home')
        except:
            return redirect('student_home')
    else:
        return render(request, 'pre_home/index.html', {"categories": item[0], "images": item[1]})


def contactus(request):
    return render(request, 'pre_home/contactus.html')


def services(request):
    return render(request, 'pre_home/services.html')


def about(request):
    return render(request, 'pre_home/about.html')

def parentsession(request):
    return render(request, 'pre_home/parentsession.html')
