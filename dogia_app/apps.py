from django.apps import AppConfig


class DogiaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dogia_app'

    def ready(self):
        import dogia_app.signals  # Adicione esta linha para importar os sinais