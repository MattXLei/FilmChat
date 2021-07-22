from django.core.serializers.python import Serializer
from django.core.paginator import Paginator
from django.core.serializers import serialize
import asyncio
from asgiref.sync import sync_to_async

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
import json
from django.contrib.auth import get_user_model
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
from django.utils import timezone
from datetime import datetime

from public_chat.models import PublicChatRoom, PublicRoomChatMessage

User = get_user_model()
"""Constants Below"""
MSG_TYPE_MESSAGE = 0 # For standard messages with no errors
MSG_TYPE_CONNECTED_USER_COUNT = 1 # For sending the connected user count
DEFAULT_ROOM_CHAT_MESSAGE_PAGE_SIZE = 30 # 30 messages per chat loading


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

		self.room_id = None # ADDED FOR DEFAULT VALUE SET; removed everything below
		

	async def disconnect(self, code):
		"""
		Called when the WebSocket closes for any reason.
		"""
		# leave the room
		print("PublicChatConsumer: disconnect")

		#ADDED THIS BELOW: 
		try:
			if self.room_id != None:
				await self.leave_room(self.room_id)
		except Exception:
			pass
	

	async def receive_json(self, content):
		"""
		Called when we get a text frame. Channels will JSON-decode the payload
		for us and pass it as the first argument.
		"""
		# Messages will have a "command" key we can switch on; only person who causes error will see it
		command = content.get("command", None)
		print("PublicChatConsumer: receive_json: " + str(command))
		try:
			if command == "send":
				if len(content["message"].lstrip()) != 0:
					await self.send_room(content["room_id"], content["message"])
			elif command == "join":
				await self.join_room(content['room'])
			elif command == "leave":
				await self.leave_room(content['room'])
			elif command == "get_room_chat_messages":
				await self.display_progress_bar(True) # Shows progress bar while waiting for more chat messages to load
				room = await get_room_or_error(content['room_id'])
				payload = await get_room_chat_messages(room, content['page_number'])
				if payload != None: # If messages, send messages to payload. Else, exception
					payload = json.loads(payload)
					await self.send_messages_payload(payload['messages'], payload['new_page_number'])
				else:
					raise ClientError(204, "Something went wrong retrieving chatroom messages.")
				await self.display_progress_bar(False) # Stops showing progress bar when messages finish loading

		except ClientError as e:
			await self.display_progress_bar(False)
			await self.handle_client_error(e) # Added Today  since function created to handle these Client Errors

	async def send_room(self, room_id, message): #  renamed to send_room instead of send_message adding room_id parameter
		print("PublicChatConsumer: send_room")

		if self.room_id != None: # Checking if user is sending message in room that they're not in
			if str(room_id) != str(self.room_id):
				raise ClientError("ROOM_ACCESS_DENIED", "Room Access Denied.")
			if not is_authenticated(self.scope['user']):
				raise ClientError("AUTH_ERROR", "You must be authenticated to chat.")
		else:
			raise ClientError("ROOM_ACCESS_DENIED", "Room Access Denied.")

		room = await get_room_or_error(room_id)
		await create_public_room_chat_message(room, self.scope['user'], message)

		await self.channel_layer.group_send(
			room.group_name, # Replaced string with this 
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


#Connect and subscribe to specific room. STARTING HERE IS MULTIPLE CHATS STUFF (do Private Chat section LATER)

	async def join_room(self, room_id): # Called by receive_json when someone sends Join command
		print("PublicChatConsumer: join_room")

		is_auth = is_authenticated(self.scope['user'])

		try:
			room = await get_room_or_error(room_id)
		except ClientError as e:
			await self.handle_client_error(e)

		# Add user to "users" list connected for room
		if is_auth:
			await connect_user(room, self.scope['user'])
		
		self.room_id = room.id # Stores the fact that a user is in the room

		await self.channel_layer.group_add( # Adds people to group to see room messages
			room.group_name,
			self.channel_name
		)

		# Tell client to finish opening the chat room; will work for private chats
		await self.send_json({
			"join": str(room.id),
			#"username": self.scope['user'].username
		})

		"""num_connected_users = get_num_connected_users(room)
		await self.channel_layer.group_send(
			room.group_name,
			{
				"type": "connected.user.count", # Connected_user_count
				#"connected_user_count": num_connected_users,
			}
		)"""

	async def leave_room(self, room_id): # Called by receive_json when someone sends a LEAVE command
		print("PublicChatConsumer: leave_room")
		is_auth = is_authenticated(self.scope['user'])
		room = await get_room_or_error(room_id)

		if is_auth: # Remove user
			await disconnect_user(room, self.scope['user'])

		self.room_id = None # Remove that user is in room
		await self.channel_layer.group_discard( # User can no longer receive messages when leave group
			room.group_name,
			self.channel_name
		)

		"""num_connected_users = get_num_connected_users(room)
		await self.channel_layer.group_send(
			room.group_name,
			{
				"type": "connected.user.count", # Connected_user_count
				"connected_user_count": num_connected_users,
			}
		)"""

	async def handle_client_error(self, e): # Called when ClientError is raised; sends error data to UI
		errorData = {}
		errorData['error'] = e.code
		if e.message:
			errorData['message'] = e.message
			await self.send_json(errorData)
		return

	async def send_messages_payload(self, messages, new_page_number): # Sends payload of messages to UI
		print("PublicChatConsumer: send_messages_payload.")
		await self.send_json({
			"messages_payload": "messages_payload",
			"messages": messages,
			"new_page_number": new_page_number,
		})

	async def display_progress_bar(self, is_displayed): # Loads progress circular bar when scrolling up in chat messages to see more
		print("DISPLAY PROGRESS BAR: " + str(is_displayed))
		await self.send_json({
			"display_progress_bar": is_displayed,

		})

	async def connected_user_count(self, event): # Makes payload of connected user amount and sends to the UI
		print("PublicChatConsumer: connected_user_count: " + str(event['connected_user_count']))
		await self.send_json({
			"msg_type": MSG_TYPE_CONNECTED_USER_COUNT,
			"connected_user_count": event['connected_user_count']
		})


def is_authenticated(user):
	if user.is_authenticated:
		return True
	return False


"""def get_num_connected_users(room): # Returns number of active users in the chat room
	try:
		if room.users:
			print(room.users.filter())
			return len(room.users.all())
		return 0
	except Exception as e:
		print(e)"""

@database_sync_to_async # Saves chat messages to database
def create_public_room_chat_message(room, user, message):
	return PublicRoomChatMessage.objects.create(user = user, room = room, content = message)

@database_sync_to_async # Converts synchronous functions (anything accessing database tables) to asynchronous functions
def connect_user(room, user): # Displaying count of connected users
	return room.connect_user(user) # In models.py from public_chat.

@database_sync_to_async
def disconnect_user(room, user):
	return room.disconnect_user(user)

@database_sync_to_async
def get_room_or_error(room_id): # Tries getting room
	try:
		room = PublicChatRoom.objects.get(pk=room_id)
	except PublicChatRoom.DoesNotExist:
		raise ClientError("ROOM_INVALID", "Invalid Room")
	return room


@database_sync_to_async
def get_room_chat_messages(room, page_number): # Get page number; checks if less than total # of pages that is calculated by Paginator and might add chat message data to the database given specific page number
	try:
		qs = PublicRoomChatMessage.objects.by_room(room) # Makes QuerySet getting messages by room
		messages_data = None
		p = Paginator(qs, DEFAULT_ROOM_CHAT_MESSAGE_PAGE_SIZE)

		payload = {}
		new_page_number = int(page_number)
		if new_page_number <= p.num_pages:
			new_page_number = new_page_number + 1
			s = LazyRoomChatMessageEncoder()
			payload['messages'] = s.serialize(p.page(page_number).object_list)
		else:
			payload['messages'] = "None"
		payload['new_page_number'] = new_page_number

		return json.dumps(payload)

	except Exception as e:
		print("EXCEPTION: " + str(e))
		return None

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
	return str(ts)

class LazyRoomChatMessageEncoder(Serializer): # Convert stuff to JSON first
	def get_dump_object(self, obj):
		dump_object = {}
		dump_object.update({'msg_type': MSG_TYPE_MESSAGE})
		dump_object.update({'msg_id': str(obj.id)})
		dump_object.update({'user_id': str(obj.user.id)})
		dump_object.update({'username': str(obj.user.username)})
		dump_object.update({'message': str(obj.content)})
		dump_object.update({'profile_image': str(obj.user.profile_image.url)})
		dump_object.update({'natural_timestamp': calculate_timestamp(obj.timestamp)})
		return dump_object