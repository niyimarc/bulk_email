from django.urls import path
from .views import send_email_view

urlpatterns = [
    path('send_email/<int:pk>/', send_email_view, name='send_email'),
]
