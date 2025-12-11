from django.db import models
from django.contrib.auth.models import User

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
 

class comment(models.Model):
    # related_name='comments' permet d'accéder aux commentaires depuis postModel
    # via `post.comments` (plutôt que comments_set), ce qui est plus lisible.
    post = models.ForeignKey(postModel, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'