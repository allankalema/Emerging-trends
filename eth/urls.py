from django.urls import path
from .views import wallet_balance, register_student, view_student

urlpatterns = [
    path('wallet/', wallet_balance, name='wallet_balance'),
    path('register/', register_student, name='register_student'),
    path('view/', view_student, name='view_student'),
    
]