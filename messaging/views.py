from django.shortcuts import render, redirect #render → show HTML page/     redirect → move to another page
from django.contrib.auth.models import User   #User → Django users
from .models import Message   #Message → your model (database table)


def messaging_main(request):
    view = request.GET.get('view', 'inbox')

    # Handle sending message
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        receiver_username = request.POST.get('receiver')
        receiver = User.objects.get(username=receiver_username)

        Message.objects.create(
            subject=subject,
            body=body,
            sender=request.user,
            receiver=receiver
        )
        return redirect('/messaging/?view=inbox')

    # Prepare context
    context = {
        'view_type': view,
        'users': User.objects.all()
    }

    if view == 'inbox':
        context['messages'] = Message.objects.filter(receiver=request.user).order_by('-timeStamp')
    elif view == 'sent':
        context['sent_messages'] = Message.objects.filter(sender=request.user).order_by('-timeStamp')

    return render(request, 'messaging/main.html', context)






# # To send a message
# #def send_message(request):
    
#     if request.method == "POST":
#         subject = request.POST['subject']
#         body = request.POST['body']
#         receiver_username = request.POST['receiver']

#         receiver = User.objects.get(username=receiver_username)

#         msg = Message(

#             subject=subject,
#             body=body,
#             sender=request.user,
#             receiver=receiver
#         )

#         msg.save()


#         return redirect('inbox')

#     users = User.objects.all()
#     return render(request, 'messaging/send_message.html', {'users': users})



# #def inbox(request):
#     messages = Message.objects.filter(receiver=request.user).order_by('-timeStamp')
#     return render(request, 'messaging/inbox.html', {'messages': messages})