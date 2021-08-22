from django.urls import path

from .views import(
    public_chat_room_view
)

app_name = "public_chat"

urlpatterns = [
    path('', public_chat_room_view, name="public-chat-room"),
]
