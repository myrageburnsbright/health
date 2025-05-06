from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from physician.models import Doctor
from patient.models import Patient

from .forms import UserLoginForm, UserRegisterForm
from .models import User

def logout_view(request):
    logout(request)
    messages.success(request, 'You were logged out')
    return redirect('/')

def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in')
        return redirect('/')
    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request=request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are logged in')
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
        
            messages.error(request, 'Error when logging in, no user with these credentials')
        else:
            messages.error(request, 'Error when logging in')
    else:
        form = UserLoginForm()
    
    context = {
        'form': form
    }
    return render(request, 'userauths/sign-in.html', context)
    
def register_view(request):
    if request.user.is_authenticated:
        messages.success(request, 'You are already logged in')
        return redirect('/')
    if request.method == 'POST':
        form = UserRegisterForm(data = request.POST)
        if form.is_valid():
            form.save()
            full_name = form.cleaned_data.get('full_name')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user_type = form.cleaned_data.get('user_type')
            user = authenticate(request=request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user_type == 'Patient':
                    Patient.objects.create(user=user, full_name=full_name, email=email)
                elif user_type == 'Doctor':
                    Doctor.objects.create(user=user, full_name=full_name, email=email)
                messages.success(request, 'You are registered')
            return redirect('/')
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }

    return render(request, 'userauths/sign-up.html', context)