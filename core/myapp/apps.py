from django.apps import AppConfig


class MyappConfig(AppConfig):
    """Configuration for app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp"

    def ready(self):
        """Call when start app."""
        import myapp.signals  # noqa: ignore=F401
