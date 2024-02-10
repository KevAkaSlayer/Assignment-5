from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Borrow
from .forms import UserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from . import forms

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully')
            return redirect('login')
    
    else:
        form = forms.UserForm()
    return render(request, 'signup.html', {'form' : form, 'type' : 'Register'})


class UserLoginView(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return reverse_lazy('home')

@login_required(login_url='login')   
def LogoutView(request):
    logout(request)
    messages.warning(request,'Logged out Successfully')
    return redirect ('login')

@login_required(login_url='login')
def profile(request):
    borrowed_instance = Borrow.objects.filter(user = request.user)
    borrowed_instance_count = Borrow.objects.filter(user =request.user,type = "Borrowed").count

    return render(request,'profile.html',{'borrowed_instance' : borrowed_instance,'count':borrowed_instance_count})