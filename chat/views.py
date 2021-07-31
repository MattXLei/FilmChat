from django.shortcuts import render, redirect
from django.conf import settings
from itertools import chain
from django.http import HttpResponse
import json

from account.models import Account
from chat.models import PrivateChatRoom, RoomChatMessage
from chat.utils import find_or_create_private_chat

DEBUG = False

def private_chat_room_view(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")

    #1 Find all rooms the user is in; get both users
    rooms1 = PrivateChatRoom.objects.filter(user1= user, is_active = True)
    rooms2 = PrivateChatRoom.objects.filter(user2 = user, is_active = True)

    #2 Merge the lists so they're unique with no duplicates
    rooms = list(chain(rooms1, rooms2))

    #3 New data structure: m_and_f, messages and friends. [{"message": "hey", "friend": "Mitch"}, ...]
    m_and_f = []
    for room in rooms:
        # Distinguish between both users
        if room.user1 == user:
            friend = room.user2
        else:
            friend = room.user1
        m_and_f.append({
            "message": "", # Come back and change
            "friend": friend,
        })

    context = {}
    context['debug'] = DEBUG # Shows chat page number
    context['debug_mode'] = settings.DEBUG # Whether in debug mode or not from settings.py perspective
    context['m_and_f'] = m_and_f

    return render(request, "chat/room.html", context)


def create_or_return_private_chat(request, *args, **kwargs):
    user1 = request.user
    payload = {}
    if user1.is_authenticated:
        if request.method == "POST":
            user2_id = request.POST.get("user2_id")
            try:
                user2 = Account.objects.get(pk=user2_id)
                chat = find_or_create_private_chat(user1, user2)
                payload['response'] = "Successfully got the chat loaded."
                payload['chatroom_id'] = chat.id
            except Account.DoesNotExist:
                payload['response'] = "Unable to start a chat with this user."
    else:
        payload['response'] = "You cannot start a chat if you aren't authenticated."
    return HttpResponse(json.dumps(payload), content_type = "application/json")