DEFAULT_NOTIFICATION_PAGE_SIZE = 15


"""
"General" notifications include:
	1. FriendRequest
	2. FriendList
"""
# New 'general' notifications data payload incoming
GENERAL_MSG_TYPE_NOTIFICATIONS_PAYLOAD = 0

# No more 'general' notifications to retrieve
GENERAL_MSG_TYPE_PAGINATION_EXHAUSTED = 1

# Retrieved all 'general' notifications newer than the oldest visible on screen
GENERAL_MSG_TYPE_NOTIFICATIONS_REFRESH_PAYLOAD = 2

# Get any new notifications
GENERAL_MSG_TYPE_GET_NEW_GENERAL_NOTIFICATIONS = 3

# Send the number of unread "general" notifications to the template
GENERAL_MSG_TYPE_GET_UNREAD_NOTIFICATIONS_COUNT = 4

# Update a notification that has been altered (Ex: Accept/decline a friend request)
GENERAL_MSG_TYPE_UPDATED_NOTIFICATION = 5


"""
"Chat" notifications include:
	1. UnreadChatRoomMessages
"""
CHAT_MSG_TYPE_NOTIFICATIONS_PAYLOAD = 10  # New 'chat' notifications data payload incoming
CHAT_MSG_TYPE_GET_NEW_NOTIFICATIONS = 13  # Get any new chat notifications
# No more 'chat' notifications to retrieve
CHAT_MSG_TYPE_PAGINATION_EXHAUSTED = 11
# number of chat notifications
CHAT_MSG_TYPE_GET_UNREAD_NOTIFICATIONS_COUNT = 14
