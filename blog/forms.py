from django import forms
from .models import postModel, comment # Assurez-vous d'importer votre modèle

class PostModelForm(forms.ModelForm):
    # Vous pouvez personnaliser les champs ici si besoin
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    # NOTE: le champ d'images est géré côté template via un input file multiple
    # et traité directement dans la vue (request.FILES.getlist('images')).
    # On ne le met pas dans les champs du ModelForm pour éviter les problèmes
    # de widget multi-upload dépendant de la version de Django.
    pass

    # C'EST CETTE PARTIE QUI MANQUE OU QUI EST INCOMPLÈTE :
    class Meta:
        model = postModel       # <--- Indispensable : le lien vers le modèle
        fields = ['title', 'content'] # <--- Liste des champs à afficher
class postUpdateform(forms.ModelForm):
    class Meta:
        model=postModel        
        fields=['title','content']

class commentForm(forms.ModelForm):

    content= forms.CharField(label="", widget=forms.TextInput (attrs={ 'rows': 5, 'placeholder': 'Ajouter un commentaire...'}))

    class Meta:
        model = comment        
        fields=['content']        