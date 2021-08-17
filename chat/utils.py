
from chat.models import PrivateChatRoom

from django.contrib.humanize.templatetags.humanize import naturalday

from datetime import datetime


def find_or_create_private_chat(user1, user2):
    try:
        chat = PrivateChatRoom.objects.get(user1=user1, user2=user2)
    except PrivateChatRoom.DoesNotExist:
        try:
            chat = PrivateChatRoom.objects.get(user1=user2, user2=user1)
        except Exception as e:
            chat = PrivateChatRoom(user1=user1, user2=user2)
            chat.save()
    return chat


# Find time stamp of chat message; if today or yesterday, add time and "today/yesterday at". Else, just put the date.
def calculate_timestamp(timestamp):
    #today or yesterday
    if (naturalday(timestamp) == "today" or (naturalday(timestamp) == "yesterday")):
        # hour (0-12):minute:(AM or PM)
        str_time = datetime.strftime(timestamp, "%I:%M %p")
        str_time = str_time.strip("0")
        ts = f"{naturalday(timestamp)} at {str_time}"
    # ts = time stamp; Before yesterday aka 24 hours ago
    else:
        str_time = datetime.strftime(timestamp, "%m/%d/%Y")  # Month/Day/Year
        ts = f"{str_time}"
    return str(ts)
