from django.apps import AppConfig  # Import the base class for app configuration


class BaseConfig(AppConfig):
    """
    Configuration class for the 'base' app. 
    This class is responsible for setting up app-level configurations and imports.
    """

    default_auto_field = 'django.db.models.BigAutoField'  # Sets the default primary key field type for models in this app
    name = 'base'  

    def ready(self):
        """
        The ready() method is called when the app is fully loaded.
        It is used to register signals so that they are recognized by the application.
        """
        import base.signals  # Import signal handlers defined in the 'signals.py' file of the 'base' app
