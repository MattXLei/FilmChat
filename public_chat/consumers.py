from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from django.contrib.auth import get_user_model
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
from django.utils import timezone
from datetime import datetime
import pytz
MSG_TYPE_MESSAGE = 0 # For standard messages with no errors

User = get_user_model()

# Example taken from:
# https://github.com/andrewgodwin/channels-examples/blob/master/multichat/chat/consumers.py
class PublicChatConsumer(AsyncJsonWebsocketConsumer):

	async def connect(self):
		"""
		Called when the websocket is handshaking as part of initial connection.
		"""
		print("PublicChatConsumer: connect: " + str(self.scope["user"]))
		# let everyone connect. But limit read/write to authenticated users
		await self.accept()

		# Add them to the group so they get room messages
		await self.channel_layer.group_add(
			"public_chatroom_1",
			self.channel_name,
		)


	async def disconnect(self, code):
		"""
		Called when the WebSocket closes for any reason.
		"""
		# leave the room
		print("PublicChatConsumer: disconnect")
		pass
	

	async def receive_json(self, content):
		"""
		Called when we get a text frame. Channels will JSON-decode the payload
		for us and pass it as the first argument.
		"""
		# Messages will have a "command" key we can switch on; only person who causes error will see it
		command = content.get("command", None)
		print("PublicChatConsumer: receive_json: " + str(command))
		print("PublicChatConsumer: receive_json: message: " + str(content["message"]))
		try:
			if command == "send":
				if len(content["message"].lstrip()) == 0:
					raise ClientError(422, "You can't send an empty message.")
				await self.send_message(content["message"])
		except ClientError as e:
			errorData = {}
			errorData['error'] = e.code
			if e.message:
				errorData['message'] = e.message
			await self.send_json(errorData)

	async def send_message(self,message):
		await self.channel_layer.group_send(
			"public_chatroom_1",
			{
				"type": "chat.message",
				"profile_image": self.scope["user"].profile_image.url,
				"username": self.scope["user"].username,
				"user_id": self.scope["user"].id,
				"message": message,
			}
		)

	async def chat_message(self, event):
		"""
		Called when someone has messaged our chat.
		"""
		# Send a message down to the client
		print("PublicChatConsumer: chat_message from user #" + str(event["user_id"]))
		timestamp = calculate_timestamp(timezone.now()) # Generates time stamp for message
		await self.send_json( # Uses these parameters to make the chat message sent to index.html
			{
				"msg_type": MSG_TYPE_MESSAGE,
				"profile_image": event["profile_image"],
				"username": event["username"],
				"user_id": event["user_id"],
				"message": event["message"],
				"natural_timestamp": timestamp,
			},
		)

class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code, message):
        super().__init__(code)
        self.code = code
        if message:
        	self.message = message


def calculate_timestamp(timestamp): #Find time stamp of chat message; if today or yesterday, add time and "today/yesterday at". Else, just put the date.
	#today or yesterday
	if (naturalday(timestamp) == "today" or (naturalday(timestamp) == "yesterday")):
		str_time = datetime.strftime(timestamp, "%I:%M %p") # hour (0-12):minute:(AM or PM)
		str_time = str_time.strip("0")
		ts = f"{naturalday(timestamp)} at {str_time}"
	#ts = time stamp; Before yesterday aka 24 hours ago
	else:
		str_time = datetime.strftime(timestamp, "%m/%d/%Y") # Month/Day/Year
		ts = f"{str_time}"
	return ts