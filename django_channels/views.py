from django.shortcuts import render
from django.views import View
from django_channels.models import Group, Chat

class ChatView(View):
    def get(self, request, group_name, *args, **kwargs):
        group = Group.objects.filter(name = group_name).first()
        chats = []

        if group:
            chats = Chat.objects.filter(group=group)
        else:
            group = Group(name = group_name)
            group.save()

        context = {}
        context["chats"] = chats
        context["group_name"] = group_name

        return render(request=request, template_name="django_channels/index.html", context=context)