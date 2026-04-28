# Created by : Mithila Hossain
# Used and written by: Ghoufran Al-Kooh
# Feature: Messaging system views
# Description: Handles inbox, send message, sent messages, drafts, reply, and search functionality

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message
from teams.models import Team
from django.db.models import Q


def messaging_main(request):
    view = request.GET.get('view', 'send')
    
    query = request.GET.get('q')  # 🔥 NEW (search input)

    # Handle sending message

    draft_to_edit = None
    edit_id = request.GET.get('edit')
    if edit_id:
       draft_to_edit = Message.objects.filter(
            id=edit_id,
            sender=request.user,
            is_draft=True
        ).first()


    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        receiver_id = request.POST.get('receiver')
        receiver = User.objects.filter(id=receiver_id).first()

        if not receiver:
            receiver = request.user   # fallback → send to yourself
            


        team_id = request.POST.get('team')
        team = None

        if team_id:
            team = Team.objects.filter(id=team_id).first()
 
        action = request.POST.get('action', 'send')

        draft_id = request.POST.get('draft_id')
        if draft_id:
            msg = Message.objects.get(id=draft_id, sender=request.user)
            msg.subject = subject
            msg.body = body
            msg.receiver = receiver
            msg.is_draft = (action == 'draft')
            msg.save()
            
        else:
            
            Message.objects.create(
                subject=subject,
                body=body,
                sender=request.user,
                receiver=receiver,
                team=team,
                is_draft=(action == 'draft')
        )
        

        return redirect('/messaging/?view=inbox')


    reply_to_id = request.GET.get('reply_to')  # grabs ?reply_to=ID from URL
    pre_receiver = None
    if reply_to_id:
        pre_receiver = User.objects.filter(id=reply_to_id).first()

    
    new_inbox_count = Message.objects.filter(
        receiver=request.user,
        is_draft=False
    ).count()
    
    new_draft_count = Message.objects.filter(
        sender=request.user,
        is_draft=True
    ).count()



        


    context = {
        'view_type': view,
        'users': User.objects.all(),
        'teams': Team.objects.all(),
        'pre_receiver': pre_receiver,
        'query': query,
        'draft': draft_to_edit,
        'new_inbox_count': new_inbox_count,
        'new_draft_count': new_draft_count,
    }
    

    page_templates = {

        'inbox': 'messaging/inbox.html',
        'send': 'messaging/sendMessage.html',
        'sent': 'messaging/sent.html',
        'draft': 'messaging/draft.html',

    }

    context['template_name'] = page_templates.get(view, 'messaging/inbox.html')

    if view == 'inbox':
        messages = Message.objects.filter(
            receiver=request.user,
            is_draft=False
            )

        if query:
           messages = messages.filter(
            Q(subject__icontains=query) |
            Q(body__icontains=query) |
            Q(sender__username__icontains=query) |
            Q(team__name__icontains=query)   # added team
        )

        context['messages'] = messages.order_by('-timeStamp')

    elif view == 'sent':
        sent = Message.objects.filter(
            sender=request.user,
            is_draft=False
            )

        if query:
            sent = sent.filter(
            Q(subject__icontains=query) |
            Q(body__icontains=query) |
            Q(receiver__username__icontains=query) |
            Q(team__name__icontains=query)   # added team
        )

        context['sent_messages'] = sent.order_by('-timeStamp')

        
    elif view == 'draft':
        context['draft_messages'] = Message.objects.filter(
            sender=request.user,
            is_draft=True
       
        ).order_by('-timeStamp')



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