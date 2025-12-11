# users/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import profileModel # Assurez-vous que le chemin vers votre modèle Profile est correct

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Cette fonction est appelée chaque fois qu'un objet User est sauvegardé.
    Si l'utilisateur vient d'être créé, on lui crée un profil.
    """
    if created:
        profileModel.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Sauvegarde le profil chaque fois que l'utilisateur est sauvegardé.
    """
    # S'assurer qu'un profile existe ; si non, le créer.
    # On utilise get_or_create pour éviter l'accès direct à
    # `instance.profileModel` qui lèverait une exception si le profil
    # n'existe pas (RelatedObjectDoesNotExist). get_or_create garantit
    # qu'une instance de profile est disponible après le save() de User.
    profileModel.objects.get_or_create(user=instance)