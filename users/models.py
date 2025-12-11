from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from PIL import Image
import os

class profileModel(models.Model):
    # AJOUT DE related_name='profile'
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile') 
    
    image = models.ImageField(
    # Par défaut, on pointe vers `media/profile_pics/default.png`.
    # Cela facilite l'affichage d'un placeholder quand l'utilisateur
    # n'a pas encore téléversé d'image.
    default='profile_pics/default.png', # utiliser une image par défaut sous media/profile_pics
    upload_to='profile_pics',
    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])]
    )

    def __str__(self):
        return f'{self.user.username} Profile'
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Protection : vérifier que l'image référencée existe sur le disque
        # avant d'essayer de l'ouvrir et la redimensionner. Sans ces
        # garde-fous, un `FileNotFoundError` peut être levé si le fichier
        # par défaut manque (ex: lors d'un clone sans dossiers media).
        try:
            img_path = self.image.path
        except (ValueError, OSError):
            # image has no path (e.g. not a file-backed ImageField)
            return

        if not os.path.exists(img_path):
            # File does not exist on disk, nothing to resize
            return

        try:
            img = Image.open(img_path)
        except (FileNotFoundError, OSError):
            return

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(img_path)