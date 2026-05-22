from django.shortcuts import render, redirect
from . forms import *
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from . models import *
from django.views import View

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form':form})
    
    def post(Self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Were Created Successfully')
            return redirect('login')
        return render(request, 'accounts/register.html')
    
class ProfileView(View):
    def get(self, request):
        profile = request.user.profile
        form = ProfileForm(instance=profile)
        return render(request, 'accounts/profile.html')
    
    def post(self, request):
        profile = request.user.profile
        form = RegisterForm(request.POST, isinstance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "PRofile Were Updated Successfully")
            return redirect('profile')
        return render(request, 'accounts/profilr.html', {'form':form})
    
def ChangePasswordView(request):
    form = ChangePasswordForm()
    if request.method == 'POST':
        user = request.user
        form = ChangePasswordForm(request.POST, isinstance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Were Change Successfully')
            return redirect('profile')
    return render(request, 'accounts/password_change.html', {'form':form})

def logout(request):
    auth_logout(request)
    messages.success(request, 'Logout Successfully')
    return redirect('login')
