from django.db import models
from django.conf import settings

class PrivateChatRoom(models.Model):
    # Starts the Private Chat with the two users and whether they are friends
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "user1")
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = "user2")

    is_active = models.BooleanField(default = True)

    #def __str__(self):
    #    return f"A chat between {user1} and {user2}."
    
    @property
    def group_name(self):
        #Returns channel group sockets will subscribe to
        return f"PrivateChatRoom-{self.id}"


class RoomChatMessageManager(models.Manager):
    #Manages all chats in the room, returning set of them
    def by_room(self, room):
        qs = RoomChatMessage.objects.filter(room = room).order_by("-timestamp")
        return qs

class RoomChatMessage(models.Model):
    #Chat message created by a user in the private room
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    room = models.ForeignKey(PrivateChatRoom, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique= False, blank = False)

    objects = RoomChatMessageManager()

    def __str__(self):
        return self.content