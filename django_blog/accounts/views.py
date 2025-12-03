# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import UserRegistrationForm, ProfileForm
from django.contrib.auth.views import LoginView, LogoutView

def register(request):
    """
    Register a new user and log them in.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # optionally log in immediately
            auth_login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('blog:index')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    """
    Display profile and allow editing profile fields and email.
    """
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        # update email on user
        email = request.POST.get('email')
        if email:
            user.email = email
            user.save()
        # update profile form (bio, profile_photo)
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile.html', {'form': form, 'user': user})


# Optionally subclass login/logout views only if you want to set templates
class MyLoginView(LoginView):
    template_name = 'accounts/login.html'

class MyLogoutView(LogoutView):
    template_name = 'accounts/logged_out.html'

