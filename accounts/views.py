from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


# Home
@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


# User Registration
def register_user(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not email or not password:
            messages.error(request, 'All required fields must be filled.')
            return redirect('register')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        if len(password) < 8:
            messages.error(request, 'Password must contain at least 8 characters.')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', ''),
            phone=request.POST.get('phone', ''),
            address=request.POST.get('address', ''),
            role='driver'
        )

        messages.success(request, 'Registration successful.')
        return redirect('login')

    return render(request, 'accounts/register.html')


# User Login
def login_user(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


# User Logout
@login_required
def logout_user(request):

    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Logged out successfully.')
        return redirect('login')

    return redirect('dashboard')


# User Profile
@login_required
def user_profile(request):

    return render(request, 'accounts/profile.html', {
        'user': request.user
    })


# Update Profile
@login_required
def update_profile(request):

    if request.method == 'POST':

        user = request.user

        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.phone = request.POST.get('phone', '')
        user.address = request.POST.get('address', '')

        if User.objects.exclude(pk=user.pk).filter(email=user.email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('update-profile')

        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']

        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'accounts/update_profile.html', {
        'user': request.user
    })


# Change Password
@login_required
def change_password(request):

    if request.method == 'POST':

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(old_password):
            messages.error(request, 'Incorrect old password.')
            return redirect('change-password')

        if len(new_password) < 8:
            messages.error(request, 'Password must contain at least 8 characters.')
            return redirect('change-password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('change-password')

        request.user.set_password(new_password)
        request.user.save()

        # Keep user logged in
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Password changed successfully.')
        return redirect('profile')

    return render(request, 'accounts/change_password.html')


# Admin Check
def is_super_admin(user):
    return user.is_authenticated and user.role == 'super_admin'


# List Users
@login_required
@user_passes_test(is_super_admin)
def list_users(request):

    users = User.objects.all().order_by('-date_joined')

    return render(request, 'accounts/users.html', {
        'users': users
    })


# User Details
@login_required
@user_passes_test(is_super_admin)
def user_detail(request, user_id):

    user = get_object_or_404(User, id=user_id)

    return render(request, 'accounts/user_detail.html', {
        'selected_user': user
    })
