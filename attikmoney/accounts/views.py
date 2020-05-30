from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login
from django.conf import settings

# Create your views here.
def register(request):
        template_name = 'register.html'
        if request.method == 'POST':
                form = RegisterForm(request.POST)
                if form.is_valid():
                        user = form.save()
                        user = authenticate(username=user.username, password=form.cleaned_data['password1'])
                        login(request, user)
                        return redirect('core:dashboard')
        else:
                form = RegisterForm()
        context = {
                'form': form
        }
        return render(request, template_name, context)

def forgotpassword(request):
        template_name = 'forgot-password.html'
        if request.method == 'POST':
                form = PasswordChangeForm(request.POST)
                if form.is_valid():
                        form.save()
                        return redirect(settings.LOGIN_URL)
        else:
                form = PasswordChangeForm
        context = {
                'form': PasswordChangeForm()
        }
        return render(request, template_name, context)