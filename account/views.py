from django.shortcuts import render,redirect
from django.core.mail import EmailMultiAlternatives
# from .models import UserAccount
from .forms import Deposit
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse_lazy
# from django.views.generic import CreateView

# Create your views here.


def send_transaction_email(user,amount,subject,template):
    message = render_to_string(template,{
        'user' : user,
        'amount': amount,
    })
    send_email = EmailMultiAlternatives(subject,'',to = [user.email])
    send_email.attach_alternative(message,"text/html")
    send_email.send()

@login_required(login_url='login')
def deposit(request):
    form = Deposit
    if request.method == 'POST':
        form = Deposit(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user = request.user
            user.account.balance += amount
            user.account.save()
            messages.success(request,'Money has been deposited successfully')
            send_transaction_email(user,amount,'Deposit Confirmation','depositemail.html')
            return redirect('home')
    return render(request,'deposit.html',{'form':form})
    
    # class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    #     template_name = 'transactions/transaction_form.html'
    #     model = Transaction
    #     title = ''
    #     success_url = reverse_lazy('transaction_report')

    #     def get_form_kwargs(self):
    #         kwargs = super().get_form_kwargs()
    #         kwargs.update({
    #             'account': self.request.user.account
    #         })
    #         return kwargs

    #     def get_context_data(self, **kwargs):
    #         context = super().get_context_data(**kwargs) # template e context data pass kora
    #         context.update({
    #             'title': self.title
    #         })

    #         return context