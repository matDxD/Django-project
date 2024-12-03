from django.apps import AppConfig


class MenuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'menu'

    def ready(self):
        # Importa señales aquí para asegurarte de que se carguen cuando la aplicación esté lista
        import menu.signals
