from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length = 100,unique = True ,null = True ,blank = True)

    def __str__(self):
        return f'{self.name}'



class Book(models.Model):
    image = models.ImageField(upload_to='Books/images/',blank = True,null = True)
    title = models.CharField(max_length = 50)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

class Comment(models.Model):
    book = models.ForeignKey(Book,on_delete = models.CASCADE,related_name = 'comments')
    user = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'comments',null = True)

    Comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True ,blank = True)
    

