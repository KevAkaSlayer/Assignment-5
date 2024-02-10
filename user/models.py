from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from .constants import BORROW_CHOICES
# Create your models here.

class Borrow(models.Model):
    user = models.ForeignKey(User,related_name = 'borrow',on_delete = models.CASCADE) 
    book = models.ForeignKey(Book,related_name = 'book',on_delete = models.CASCADE) 
    type = models.CharField(max_length = 10,choices = BORROW_CHOICES) 
    time = models.DateTimeField(auto_now_add = True)