from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from PIL import Image as PilImage
import os

# Create your models here.
class postModel(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # NOTE: le champ 'author' est défini pour lier le post à un User.
    # Il apparaît deux fois ici car une modification antérieure l'a dupliqué ;
    # laisser tel quel évite de perturber les migrations existantes, mais
    # il serait propre de garder une seule déclaration si vous voulez nettoyer.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    # Les images sont maintenant une relation ManyToMany vers le modèle `Image`.
    images = models.ManyToManyField('Image', related_name='posts', blank=True)

    # (duplication présente — conservée pour compatibilité locale)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_created']  # Newest posts first by date_c
    

    def __str__(self):
        return self.title

    def comment_count(self):
        # Retourne le nombre de commentaires liés via le related_name 'comments'.
        # On utilise le manager relationnel (self.comments) — c'est plus
        # performant et évite de définir une méthode qui masquerait le manager.
        return self.comments.count()


class PostImage(models.Model):
    """Stocke des images liées à un post (plusieurs images possibles)."""
    # Champ legacy : rename related_name to avoid collision with new postModel.images ManyToMany
    post = models.ForeignKey(postModel, related_name='legacy_images', on_delete=models.CASCADE)
    # Limiter les extensions courantes et stocker dans post_images/
    image = models.ImageField(upload_to='post_images', validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','gif'])])
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image for {self.post.title} ({self.id})'

    def save(self, *args, **kwargs):
        """Redimensionne l'image si elle est trop grande pour économiser l'espace disque."""
        super().save(*args, **kwargs)

        try:
            img_path = self.image.path
        except (ValueError, OSError):
            return

        if not os.path.exists(img_path):
            return

        try:
            img = PilImage.open(img_path)
        except (FileNotFoundError, OSError):
            return

        max_size = (1200, 1200)
        if img.height > max_size[1] or img.width > max_size[0]:
            img.thumbnail(max_size)
            img.save(img_path)

    def delete(self, *args, **kwargs):
        """Supprime le fichier du disque lorsque l'objet est supprimé."""
        try:
            img_path = self.image.path
            if os.path.exists(img_path):
                os.remove(img_path)
        except Exception:
            pass
        super().delete(*args, **kwargs)
 

class Image(models.Model):
    """Modèle centralisé pour les images, partageables entre posts (ManyToMany)."""
    image = models.ImageField(upload_to='post_images', validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','gif'])])
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image ({self.id})'

    @property
    def thumbnail_url(self):
        """URL de la miniature si présente, sinon URL de l'image originale."""
        try:
            base, ext = os.path.splitext(self.image.path)
            thumb_path = f"{base}_thumb{ext}"
            if os.path.exists(thumb_path):
                base_url, ext = os.path.splitext(self.image.url)
                return f"{base_url}_thumb{ext}"
        except Exception:
            pass
        return self.image.url

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            img_path = self.image.path
        except (ValueError, OSError):
            return

        if not os.path.exists(img_path):
            return

        try:
            img = PilImage.open(img_path)
        except (FileNotFoundError, OSError):
            return

        max_size = (1200, 1200)
        if img.height > max_size[1] or img.width > max_size[0]:
            img.thumbnail(max_size)
            img.save(img_path)

        # Générer une miniature (thumbnail) pour affichage de vignettes
        try:
            base, ext = os.path.splitext(img_path)
            thumb_path = f"{base}_thumb{ext}"
            if not os.path.exists(thumb_path):
                thumb = img.copy()
                thumb.thumbnail((300, 300))
                thumb.save(thumb_path)
        except Exception:
            pass

    def delete(self, *args, **kwargs):
        try:
            img_path = self.image.path
            if os.path.exists(img_path):
                os.remove(img_path)
            base, ext = os.path.splitext(img_path)
            thumb_path = f"{base}_thumb{ext}"
            if os.path.exists(thumb_path):
                os.remove(thumb_path)
        except Exception:
            pass
        super().delete(*args, **kwargs)


class comment(models.Model):
    # related_name='comments' permet d'accéder aux commentaires depuis postModel
    # via `post.comments` (plutôt que comments_set), ce qui est plus lisible.
    post = models.ForeignKey(postModel, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'