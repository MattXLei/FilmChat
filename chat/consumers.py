from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.serializers import serialize
from django.utils import timezone

import json

from chat.models import RoomChatMessage, PrivateChatRoom
from friend.models import FriendList
from account.utils import LazyAccountEncoder
from chat.exceptions import ClientError
from chat.utils import calculate_timestamp
from chat.constants import *


class ChatConsumer(AsyncJsonWebsocketConsumer):

	async def connect(self):
		"""
		Called when the websocket is handshaking as part of initial connection and printing the users who are connecting.
		"""
		print("ChatConsumer: connect: " + str(self.scope["user"]))

		# let everyone connect. But limit read/write to authenticated users
		await self.accept()

		# the room_id will define what it means to be "connected". If it is not None, then the user is connected.
		self.room_id = None

	async def receive_json(self, content):
		"""
		Called when we get a text frame. Channels will JSON-decode the payload
		for us and pass it as the first argument.
		"""
		# Messages will have a "command" key we can switch on
		print("ChatConsumer: receive_json")
		command = content.get("command", None)
		try:
			if command == "join":
				await self.join_room(content['room'])
			elif command == "leave":
				await self.leave_room(content['room'])
			elif command == "send":
				if len(content['message'].lstrip()) != 0:
					await self.send_room(content['room'], content['message'])
			elif command == "get_room_chat_messages":
				pass
			elif command == "get_user_info":
				room = await get_room_or_error(content['room_id'], self.scope['user'])
				payload = get_user_info(room, self.scope['user'])
				if payload != None:
					payload = json.loads(payload)
					await self.send_user_info_payload(payload['user_info'])
				else:
					raise ClientError("INVALID_PAYLOAD", "Something went wrong retrieving the other user's account data.")

		except ClientError as e:
			await self.handle_client_error(e)

	async def disconnect(self, code):
		"""
		Called when the WebSocket closes for any reason.
		"""
		# Leave the room; placeholder
		print("ChatConsumer: disconnect")
		try:
			if self.room_id != None: # In room
				await self.leave_room(self.room_id)
		except Exception as e:
			pass

	async def join_room(self, room_id):
		"""
		Called by receive_json when someone sent a join command/tries to join the room.
		"""
		# The logged-in user is in our scope thanks to the authentication ASGI middleware (AuthMiddlewareStack)
		print("ChatConsumer: join_room: " + str(room_id))

		try:
			room = await get_room_or_error(room_id, self.scope['user'])
		except ClientError as e:
			return await self.handle_client_error(e)

		# Store the fact that we're in the room
		self.room_id = room.id
		
		# Add to group so they get messages
		await self.channel_layer.group_add(
			room.group_name,
			self.channel_name
		)

		await self.send_json({ # Ready to join the chatroom
			"join": str(room.id)
		})

	async def leave_room(self, room_id):
		"""
		Called by receive_json when someone sent a leave command.
		"""
		# The logged-in user is in our scope thanks to the authentication ASGI middleware
		print("ChatConsumer: leave_room")
		room = await get_room_or_error(room_id, self.scope['user'])

		# Notify group aka other person someone left
		await self.channel_layer.group_send(
			room.group_name,
			{
				"type": "chat.leave", # chat_leave
				"room_id": room_id,
				"profile_image": self.scope['user'].profile_image.url,
				"username": self.scope['user'].username,
				"user_id": self.scope['user'].id,
			}
		)

		self.room_id = None

		# Remove from group so cannot get room messages
		await self.channel_layer.group_discard(
			room.group_name,
			self.channel_name,
		)

		await self.send_json({ # Finalize the leave as a closing statement
			"leave": str(room.id)
		})

	async def send_room(self, room_id, message):
		"""
		Called by receive_json when someone sends a message to a room.
		"""
		print("ChatConsumer: send_room")
		if self.room_id != None: # If someone is in the room and allowed to be
			if str(room_id) != str(self.room_id):
				raise ClientError("ROOM_ACCESS_DENIED", "Room access denied")
		else:
			raise ClientError("ROOM_ACCESS_DENIED", "Room access denied")

		room = await get_room_or_error(room_id, self.scope['user'])
		await create_room_chat_message(room, self.scope['user'], message)

		await self.channel_layer.group_send( # Sends message to everyone in the chat
			room.group_name,
			{ # Keywords
				"type": "chat.message",
				"profile_image": self.scope['user'].profile_image.url,
				"username": self.scope['user'].username,
				"user_id": self.scope['user'].id,
				"message": message,
			}
		)

	# These helper methods are named by the types we send - so chat.join becomes chat_join

	async def chat_join(self, event):
		"""
		Called when someone has joined our chat.
		"""
		# Send a message down to the client
		print("ChatConsumer: chat_join: " + str(self.scope["user"].id))

	async def chat_leave(self, event):
		"""
		Called when someone has left our chat.
		"""
		# Send a message down to the client
		print("ChatConsumer: chat_leave")

	async def chat_message(self, event):
		"""
		Called when someone has messaged our chat.
		"""
		# Send a message down to the client
		print("ChatConsumer: chat_message")

		timestamp = calculate_timestamp(timezone.now())

		await self.send_json({
			"msg_type": MSG_TYPE_MESSAGE,
			"username": event['username'],
			"user_id": event['user_id'],
			"profile_image": event['profile_image'],
			"message": event['message'],
			"natural_timestamp": timestamp,
		})

	async def send_messages_payload(self, messages, new_page_number):
		"""
		Send a payload/list of all previous chat messages to the ui
		"""
		print("ChatConsumer: send_messages_payload. ")

	async def send_user_info_payload(self, user_info):
		"""
		Send a payload of user information to the UI
		"""
		print("ChatConsumer: send_user_info_payload. ")
		await self.send_json({
			'user_info': user_info
		})

	async def display_progress_bar(self, is_displayed):
		"""
		1. is_displayed = True
			- Display the progress bar on UI
		2. is_displayed = False
			- Hide the progress bar on UI
		"""
		print("DISPLAY PROGRESS BAR: " + str(is_displayed))

	async def handle_client_error(self, e): # Called when ClientError is raised; sends error data to UI
		errorData = {}
		errorData['error'] = e.code
		if e.message:
			errorData['message'] = e.message
			await self.send_json(errorData)
		return


@database_sync_to_async
def get_room_or_error(room_id, user):
	# Gets a room for the user, checking permissions
	try:
		room = PrivateChatRoom.objects.get(pk = room_id)
	except PrivateChatRoom.DoesNotExist:
		raise ClientError("INVALID_ROOM", "Room Does Not Exist/Is Invalid.")
	
	# Is this user allowed into the room and are they friends?
	if user != room.user1 and user != room.user2:
		raise ClientError("ROOM_ACCESS_DENIED", "You cannot join this room.")

	friend_list = FriendList.objects.get(user = user).friends.all()
	if not room.user1 in friend_list:
		if not room.user2 in friend_list:
			raise ClientError("ROOM_ACCESS_DENIED", "You must be friends to chat.")
	
	return room


def get_user_info(room, user):
	# Retrives user info for the person you're chatting with
	try:
		# Determine who is who
		other_user = room.user1
		if other_user == user:
			other_user = room.user2
		payload = {}
		s = LazyAccountEncoder()
		# Convert Serializer to List; get first object
		payload['user_info'] = s.serialize([other_user])[0]
		return json.dumps(payload)
	except ClientError as e:
		print("EXCEPTION: " + str(e))

	return None # Get user or None

@database_sync_to_async
def create_room_chat_message(room, user, message): # Creates a chat message
	return RoomChatMessage.objects.create(user = user, room = room, content = message)