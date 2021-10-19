from django.core import exceptions
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import View
from users.models import User
from .models import Conversation, Message

def go_conversations(request, a_pk, b_pk):
    user_one = User.objects.get_or_none(pk=a_pk)
    user_two = User.objects.get_or_none(pk=b_pk)
    if user_one is not None and user_two is not None:
        # conversation = Conversation.objects.get(
        #     Q(participants=user_one) & Q(participants=user_two)
        # )
        conversation = Conversation.objects.filter(participants=user_one).filter(participants=user_two).first()
        print(conversation)
        
        if not conversation:
            print("no")
            conversation = Conversation.objects.create()
            conversation.participants.add(user_one, user_two)
            
    return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class DetailConversationView(View):
    
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404
        return render(self.request, "conversations/conversation_detail.html", {"conversation": conversation})

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        conversation = Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404
        if message is not None:
            Message.objects.create(
                message=message,
                user=self.request.user,
                conversation=conversation
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))
