from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail # send_email ,THIS IS FOR SENDING ONLY ONE MAIL, 
                                    # IF WE WANT TO SEND MULTIPLE MAILS MEANS USE   send_mass_mail 

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Create your views here.

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def registration(request):
    EUFO=UserForm()
    EPFO=ProfileForm()
    d={'EUFO':EUFO,'EPFO':EPFO}
    if request.method=='POST' and request.FILES:
        NMUFDO=UserForm(request.POST)
        NMPFDO=ProfileForm(request.POST,request.FILES)
        if NMUFDO.is_valid() and NMPFDO.is_valid():
            MUFDO=NMUFDO.save(commit=False)# to convert the data
            pw=NMUFDO.cleaned_data['password']
            MUFDO.set_password(pw) #to encript the data
            MUFDO.save()
            MPFDO=NMPFDO.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()

# SENDING OF MAILS
            
            send_mail('registration',
                       'thank you for registration',
                       'a30403799@gmail.com',
                       [MUFDO.email],
                       fail_silently=False

            ) 
            return HttpResponse('REGISTRATION IS DONE SUCCESSFULLY')
        else:
            return HttpResponse('DATA IS INVALID')
    return render(request,'registration.html',d)




# HERE WE ARE DOING USER LOGIN


def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']

        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid Credentials')

    return render(request,'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

