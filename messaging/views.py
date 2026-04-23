from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Message


def messaging_main(request):
    view = request.GET.get('view', 'inbox')
    query = request.GET.get('q')  # 🔥 NEW (search input)

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

    context = {
        'view_type': view,
        'users': User.objects.all(),
        'query': query 
    }

    if view == 'inbox':
        messages = Message.objects.filter(receiver=request.user)

        if query:
            messages = messages.filter(
                subject__icontains=query
            ) | messages.filter(
                body__icontains=query
            )

        context['messages'] = messages.order_by('-timeStamp')

    elif view == 'sent':
        sent = Message.objects.filter(sender=request.user)

        if query:
            sent = sent.filter(
                subject__icontains=query
            ) | sent.filter(
                body__icontains=query
            )

        context['sent_messages'] = sent.order_by('-timeStamp')

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