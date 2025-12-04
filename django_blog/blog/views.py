# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm, ProfileForm

# User Registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')  # replace with your home URL name
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form': form})

# User Profile
@login_required
def profile(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        user.email = request.POST.get('email', user.email)
        user.save()
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'blog/profile.html', {'form': form, 'user': user})

# Optional custom login/logout
class CustomLoginView(LoginView):
    template_name = 'blog/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'blog/logged_out.html'

