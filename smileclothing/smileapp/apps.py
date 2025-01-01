from django.apps import AppConfig


class SmileappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "smileapp"


    def ready(self):
        import smileapp.signals  # Import the signals file
