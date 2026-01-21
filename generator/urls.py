from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate/', views.generate_qr, name='generate_qr'),
    path('download/', views.download_qr, name='download_qr'),
]