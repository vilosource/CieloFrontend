from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


def user_login(request):
    """Render the login page. Authentication is handled via API calls."""
    if request.user.is_authenticated:
        return redirect('index')

    return render(request, 'users/login.html')


def user_logout(request):
    """Display logout confirmation page. Session termination handled via API."""
    messages.success(request, 'You have been successfully logged out.')
    return render(request, 'users/logout.html')


@login_required
def user_profile(request):
    """
    User profile view that displays user information.
    """
    context = {
        'page_title': 'User Profile',
        'user': request.user,
        'cielo_navigation_items': [
            {
                'label': 'Dashboard',
                'url': '/',
                'icon_class': 'mdi mdi-view-dashboard-outline'
            },
            {
                'label': 'Profile',
                'url': '/users/profile/',
                'icon_class': 'mdi mdi-account-circle'
            },
            {
                'label': 'Settings',
                'url': '#',
                'icon_class': 'mdi mdi-cog-outline'
            }
        ]
    }
    return render(request, 'users/profile.html', context)


@login_required
def change_password(request):
    """
    Change password view that handles password updates.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep user logged in
            messages.success(request, 'Your password has been successfully updated!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'users/change_password.html', {'form': form})
