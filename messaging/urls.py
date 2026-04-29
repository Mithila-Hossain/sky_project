# Author: Mithila Hossain
# Feature: Messaging URL routing
# Description: Defines URL routes for messaging pages such as send, inbox, sent, and drafts
from django.urls import path
from . import views

urlpatterns = [

    path("", views.messaging_main, name="messaging_main"),
    
]
