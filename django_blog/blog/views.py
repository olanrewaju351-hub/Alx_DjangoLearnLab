from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import UserRegistrationForm, ProfileForm  # make sure these exist
from .models import Post  # optional: used on home to list posts

def home(request):
    """
    Simple homepage: lists posts (if Post model exists) or shows a welcome message.
    """
    try:
        posts = Post.objects.all().order_by('-created_at')[:10]
    except Exception:
        posts = []
    context = {'posts': posts}
    return render(request, 'blog/home.html', context)

def register(request):
    """
    User registration view using UserRegistrationForm (ModelForm for auth.User).
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # if your form returns raw password, make sure to set_password
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            messages.success(request, 'Account created. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    """
    Login view that authenticates and logs in a user.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'blog/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def profile(request):
    """
    Profile edit page. Assumes ProfileForm is a ModelForm for your Profile model.
    """
    try:
        profile_instance = request.user.profile
    except Exception:
        profile_instance = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile_instance)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile_instance)

    return render(request, 'blog/profile.html', {'form': form})

