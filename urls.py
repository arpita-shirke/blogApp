from django.urls import path
from blogApp import views

urlpatterns = [
    path('home',views.home),
    path('dashboard',views.dashboard),
    path('update/<rid>',views.edit),
    path('delete/<rid>',views.delete),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('subscription_page',views.subscription_page),
    path('payment_page',views.payment_page),
    path('payment_success/',views.payment_success),
    

    
    
]