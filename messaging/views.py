from django.shortcuts import render, redirect #render → show HTML page/     redirect → move to another page
from django.http import HttpResponse     
from django.contrib.auth.models import User   #User → Django users
from .models import Message   #Message → your model (database table)
            


def messaging_home(request):
    return HttpResponse("Messaging homepage placeholder")



# To send a message
def send_message(request):
    
    if request.method == "POST":
        subject = request.POST['subject']
        body = request.POST['body']
        receiver_username = request.POST['receiver']

        receiver = User.objects.get(username=receiver_username)

        msg = Message(

            subject=subject,
            body=body,
            sender=request.user,
            receiver=receiver
        )

        msg.save()


        return redirect('inbox')

    users = User.objects.all()
    return render(request, 'messaging/send_message.html', {'users': users})



def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-timeStamp')
    return render(request, 'messaging/inbox.html', {'messages': messages})