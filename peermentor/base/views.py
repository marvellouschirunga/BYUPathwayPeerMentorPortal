# Import necessary Django modules for views, authentication, and model interactions
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.utils import timezone


# Imports for email verification
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token

# -------------------------
# USER AUTHENTICATION VIEWS
# -------------------------

def loginPage(request):
    #Handles user login functionality.
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            user.is_online = True  # Mark user as online
            user.last_login = timezone.now()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect.')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    #Logs the user out and redirects to the homepage.
    user = request.user
    if user.is_authenticated:
        user.is_online = False  # Mark user as offline
        user.save()
    logout(request)
    return redirect('home')


def registerPage(request):
    # Handles user registration and email activation link generation.
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User must activate via email
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('home')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def activateEmail(request, user, to_email):
    """Sends an email to the user with an account activation link."""
    mail_subject = 'Activate your PeerMentor.io user account.'
    message = render_to_string('base/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Please check your email {to_email} to activate your account.')
    else:
        messages.error(request, f'Problem sending email to {to_email}. Please check if the email is correct.')

def activate(request, uidb64, token):
    """Handles email account activation via the activation link."""
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully. You can now log in.')
        return redirect('loginPage')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('home')

# -------------------------
# CORE APPLICATION VIEWS
# -------------------------

@login_required(login_url='login')
def home(request):
    """Displays the homepage, allowing users to see all rooms and messages."""
    q = request.GET.get('q') if request.GET.get('q') else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()[:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[:3]

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    """Displays a single room's details, messages, and participants."""
    room = Room.objects.get(id=pk)
    # Optimize the query to include user data efficiently
    room_messages = room.message_set.select_related('user').all()
    participants = room.participants.all()

    # Handle POST request for creating a message
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        request.user.is_online = True  # Update the user's online status
        request.user.save(update_fields=['is_online'])  # Save the change
        return redirect('room', pk=room.id)

    # Render the template with the updated context
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)



def userProfile(request, pk):
    """Displays the profile of a specific user."""
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    """Allows authenticated users to create a new chat room."""
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    """Allows users to update the details of an existing room."""
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed to edit this room.')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    """Allows users to delete an existing room."""
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed to delete this room.')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    """Allows users to delete a specific message in a room."""
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to delete this message.')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    """Allows users to update their profile information."""
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    """Displays all available discussion topics."""
    q = request.GET.get('q') if request.GET.get('q') else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    """Displays recent activity, including new messages and room updates."""
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
