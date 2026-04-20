from django.urls import path
from . import views

urlpatterns = [

    path("", views.messaging_main, name="messaging_main"),
   # path('send/', views.send_message, name='send_message'),
   # path('inbox/', views.inbox, name='inbox'),

    
]
