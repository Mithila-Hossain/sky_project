from django.urls import path
from . import views

urlpatterns = [

    path("", views.messaging_home, name="messaging_home"),
    path('send/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    
]
