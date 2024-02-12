from django.urls import path
from .import views
urlpatterns = [
    path('register/', views.register.as_view(),name = 'signup'),
    path('login/', views.UserLoginView.as_view(),name = 'login'),
    path('logout/', views.LogoutView,name = 'logout'),
    path('profile/', views.profile,name = 'profile'),
]