from django.contrib import admin  
from .models import Room, Topic, Message, User

# Register the User model with the admin site to allow admin users to manage User data
admin.site.register(User)

# Register the Room model with the admin site to allow admin users to create, read, update, and delete (CRUD) Room records
admin.site.register(Room)

# Register the Topic model with the admin site to enable admin users to manage topics associated with rooms
admin.site.register(Topic)

# Register the Message model to allow admin users to view and manage user messages in rooms
admin.site.register(Message)
