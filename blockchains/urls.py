from django.urls import path
from . import views

urlpatterns = [
    path('', views.blockchain_view, name='home'),
    path('hashing/', views.hashing_view, name='hashing_view'),
    path('signature/', views.signature_view, name='signature_view'),
]
