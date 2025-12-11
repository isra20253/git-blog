from django.apps import AppConfig

class UsersConfig(AppConfig):  # <--- CORRECTION (Grand U)
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    def ready(self):
        import users.signals  # <--- AJOUTER CETTE LIGNE POUR SIGNALS