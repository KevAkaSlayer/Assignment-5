from django.shortcuts import render,redirect
from .models import Book,Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from user.models import Borrow
from .forms import CommentForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.


def send_transaction_email(user,Book,subject,template):
    message = render_to_string(template,{
        'user': user,
        'book': Book
    })
    send_email = EmailMultiAlternatives(subject,'',to = [user.email])
    send_email.attach_alternative(message,"text/html")
    send_email.send()


def detail(request,id):
    book = Book.objects.get(pk=id)
    print(book.title)
    comments = Comment.objects.filter(book=book)

    if request.user.is_authenticated :
        has_borrowed = Borrow.objects.filter(user= request.user,book_id = id).exists()
        borrowed_count = Borrow.objects.filter(user = request.user,book_id = id,type = 'Borrowed').count()
        return_count = Borrow.objects.filter(user = request.user,book_id = id,type = 'Returned').count()

        if borrowed_count > return_count :
            possible_return = True
        else :
            possible_return = False
        return render (request,'book_details.html',{'book':book,'comment':comments,'borrowed':has_borrowed,'possible_return':possible_return})
    else :
        return render (request,'book_details.html',{'book':book,'comment':comments})
@login_required(login_url='login')
def buy(request,id):
    book =  Book.objects.get(pk=id)
    user = request.user 
    if user.account.balance>=book.price:
        borrowed_count = Borrow.objects.filter(user = request.user,book_id = id,type = 'Borrowed').count()
        return_count = Borrow.objects.filter(user = request.user,book_id = id,type = 'Returned').count()

        if borrowed_count == return_count :
            user.account.balance -= book.price
            user.account.save()
            Borrow.objects.create(user=user,type = 'Borrowed',book = book)
            messages.success(request,'Book successfully Borrowed')
            send_transaction_email(request.user,book,'Book borrow confirmation','borrow_email.html')
            return redirect('detail',id = id)
        else :
            messages.error(request,'You have to return your previous copy that u,ve borrowed')
            return redirect('detail',id = id)
    
    else :
        messages.error(request,'Not enough money!')
        return redirect('deposit')
    
@login_required(login_url='login')
def ReturnBook(request,id):
    user = request.user
    book = Book.objects.get(pk = id)
    borrowed_count = Borrow.objects.filter(user=request.user, type='Borrowed').count()
    return_count = Borrow.objects.filter(user=request.user, type='Returned').count()

    if borrowed_count > return_count :
        user.account.balance += book.price
        user.account.save()
        messages.success(request,'book returned')
        Borrow.objects.create(user = user,type = 'Returned',book = book)
        return redirect('detail',id = id)
    else :
        messages.error(request,'Borrow Book First')
        return redirect('detail',id = id)
    
@login_required(login_url='login')
def comment(request,id):
    form =CommentForm
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            book = Book.objects.get(pk= id)
            cmnt = form.cleaned_data['comment']
            Comment.objects.create(user = request.user,Comment = cmnt,book=book)
            return redirect('detail',id = id)
        return render(request,'comment.html',{'form':form})