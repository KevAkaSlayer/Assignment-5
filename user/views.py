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
from account.models import UserAccount

# Create your views here.
# def register(request):
#     if request.method == 'POST':
#         form = forms.UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Account Created Successfully')
#             return redirect('login')
    
#     else:
#         form = forms.UserForm()
#     return render(request, 'signup.html', {'form' : form, 'type' : 'Register'})

class register(CreateView):
    model = User
    template_name = 'signup.html'
    form_class= UserForm
    success_url= reverse_lazy('home')
    def form_valid(self, form):
        our_user = super().form_valid(form)
        UserAccount.objects.create(user=self.object)
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(self.request, user)

        return our_user


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
    borrowed_instances = Borrow.objects.filter(user=request.user)
    borrowed_instances_count = Borrow.objects.filter(user=request.user, type='Borrowed').count

    return render(request,'profile.html',{'borrowed_instances' :borrowed_instances,'count':borrowed_instances_count})