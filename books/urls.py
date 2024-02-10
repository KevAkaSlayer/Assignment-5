from django.urls import path
from . import views
urlpatterns = [
    path('detail/<int:id>', views.detail,name = 'detail'),
    path('buy/<int:id>', views.buy,name = 'buy'),
    path('return/<int:id>', views.ReturnBook,name = 'return'),
    path('comment/<int:id>', views.comment,name = 'comment'),
]