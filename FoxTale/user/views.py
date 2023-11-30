from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import Http404

from .forms import UserRegistrationForm, UserPasswordChangeForm, UserEmailChangoForm
from .models import UserProfileModel
import random

from django.core.mail import send_mail
# Create your views here.

def RegistrationUserView(request):
    if request.user.is_authenticated:
        raise Http404()
    else:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                form.save()
                return redirect('home')
        else:
            form = UserRegistrationForm()
    return render(request, 'registration_page.html', {'form':form})

def varification_code_generate():
    generate_code = str(random.randint(10000, 99999))
    return ''.join(generate_code)

def UserProfileVarification(request):
    try:
        if request.user.is_authenticated:
            user_entered_code = request.POST['verification_code_form']
            user_profile = UserProfileModel
            if user_profile.varification_code == user_entered_code:
                return redirect('profile')
        else:
            user = request.user
            varification_code = varification_code_generate()
            user_profile = UserProfileModel.objects.get(user=user)
            user_profile.varification_code = varification_code
            user_profile.save()

            subject = 'verification code'
            message = f'Ваш код верификации: {varification_code}'
            from_email = 'AnisimovLKA@yandex.ru'
            to_email = user.email

            send_mail(subject, message, from_email, [to_email])
        
        return render(request, 'profile/profile_varification.html')
    except:
        return redirect('home')

def ProfileView(request):
    user = request.user
    email_exist_error = ""

    try:
        user_profile = UserProfileModel.objects.get(user=user)
    except:
        user_profile = None
    
    form_change_password = UserPasswordChangeForm
    form_change_email = UserPasswordChangeForm
    if request.method == 'POST':
        if form_change_password.is_valid():
            user = form_change_password.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
        else:
            form_change_password = UserPasswordChangeForm(request.user)

        if form_change_email.is_valid():
            user = request.user
            if User.objects.filter(email=request.POST.get('new_email')).exlued(username=user.username).exists():
                email_exist_error = "email already exist"
                messages.error(request, 'Email already exist')
            else:
                user.email = request.POST.get('new_email')
                user.save()
                messages.success(request, 'Email updated')

    return render(request, 'profile/profile.html', {'user_profile': user_profile, 'form_change_password': form_change_password, 'form_change_email': form_change_email, 'email_exist_error': email_exist_error})