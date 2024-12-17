from django.forms import ModelForm  # Import Django's ModelForm to create forms from models
from django.contrib.auth.forms import UserCreationForm  # Import Django's built-in user creation form
from .models import Room, User  # Import the Room and User models used to create forms


class MyUserCreationForm(UserCreationForm):
    """
    Custom user creation form to register new users. 
    This form extends Django's default UserCreationForm and adds custom fields like name, username, and email.
    """

    class Meta:
        """
        Meta class defines the model and fields used in this form.
        """
        model = User  # Use the custom User model
        fields = ['name', 'username', 'email', 'password1', 'password2']  # Fields to be displayed and collected from the user


class RoomForm(ModelForm):
    """
    Form for creating and updating Room objects. 
    This form allows the user to input data for all fields except 'host' and 'participants' which are auto-managed.
    """

    class Meta:
        """
        Meta class defines the model and fields used in this form.
        """
        model = Room  # Use the Room model to create and update room objects
        fields = '__all__'  # Include all fields in the form
        exclude = ['host', 'participants']  # Exclude 'host' and 'participants' because they are auto-populated in the view


class UserForm(ModelForm):
    """
    Form for updating user profile information. 
    This form allows users to edit their profile details, including avatar, name, username, email, and bio.
    """

    class Meta:
        """
        Meta class defines the model and fields used in this form.
        """
        model = User  # Use the custom User model
        fields = ['avatar', 'name', 'username', 'email', 'bio']  # Fields to be displayed and updated by the user
