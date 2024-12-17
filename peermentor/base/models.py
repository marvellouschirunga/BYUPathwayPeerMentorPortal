from django.db import models  # Import Django's ORM models
from django.contrib.auth.models import AbstractUser  # Import Django's customizable user model

# User model
class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    Adds additional fields specific to this project, such as name, email, bio, avatar, and online status.
    """

    STATUS = (
        ('PM', 'PM'),  # Peer Mentor
        ('PMSA', 'PMSA'),  # Peer Mentor Support Agent
        ('SM', 'SM')  # Support Manager
    )

    name = models.CharField(max_length=200, null=True)  # Full name of the user
    email = models.EmailField(unique=True, null=True)  # User's unique email, which serves as the username
    bio = models.TextField(null=True)  # Short biography of the user
    is_online = models.BooleanField(default=False)  # Tracks if the user is currently online
    avatar = models.ImageField(null=True, default="avatar.svg")  # Profile image or avatar for the user

    # Override the default username field to use email for authentication
    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []  # No extra required fields apart from email

    def __str__(self):
        """
        String representation of the user object.
        Returns the user's name if available, otherwise the user's email.
        """
        return self.name if self.name else self.email


class Topic(models.Model):
    """
    Topic model to categorize rooms. 
    Each room is assigned a topic, and users can search or filter rooms based on topics.
    """

    name = models.CharField(max_length=200)  # The name of the topic (e.g., "Python", "Django", etc.)

    def __str__(self):
        """
        String representation of the topic object.
        Returns the topic name.
        """
        return self.name


class Room(models.Model):
    """
    Room model representing a discussion room where users can join and post messages.
    Rooms are categorized by a topic and have a host who is responsible for managing the room.
    """

    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # The user who created the room
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)  # The topic this room is associated with
    name = models.CharField(max_length=200)  # The name of the room
    description = models.TextField(null=True, blank=True)  # Detailed description of the room
    participants = models.ManyToManyField(User, related_name='participants', blank=True)  # Users currently in the room
    updated = models.DateTimeField(auto_now=True)  # Automatically updates when the room is updated
    created = models.DateTimeField(auto_now_add=True)  # Automatically sets when the room is created

    class Meta:
        """
        Meta options to specify the ordering of the rooms.
        Rooms are ordered by the most recently updated and created.
        """
        ordering = ['-updated', '-created']  # Order rooms by most recent updates and creations

    def __str__(self):
        """
        String representation of the room object.
        Returns the name of the room.
        """
        return self.name


class Message(models.Model):
    """
    Message model representing user messages posted inside a room.
    Messages are associated with a specific user and room, and contain the message body.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who posted the message
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # The room where the message was posted
    body = models.TextField()  # The text content of the message
    updated = models.DateTimeField(auto_now=True)  # Automatically updates when the message is edited
    created = models.DateTimeField(auto_now_add=True)  # Automatically sets when the message is created

    class Meta:
        """
        Meta options to specify the ordering of messages.
        Messages are ordered by the most recent updates and creations.
        """
        ordering = ['-updated', '-created']  # Order messages by most recent updates and creations

    def __str__(self):
        """
        String representation of the message object.
        Returns the first 50 characters of the message body.
        """
        return self.body[0:50]
