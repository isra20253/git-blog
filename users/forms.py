# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import profileModel

# --- Formulaire 1 : Inscription ---
class signUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    # La classe Meta est correctement indentée à l'intérieur de signUpForm
    class Meta(UserCreationForm.Meta):
        model = User
        # CORRECTION : On ne liste que les champs du modèle.
        # UserCreationForm s'occupe tout seul des mots de passe.
        fields = ('username', 'email')

    # Cette fonction pour enlever les textes d'aide est correcte, mais on la simplifie
    def __init__(self, *args, **kwargs):
        super(signUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        # Les champs de mot de passe sont ajoutés par le formulaire parent,
        # on peut y accéder comme ceci :
        if 'password1' in self.fields:
            self.fields['password1'].help_text = None
        if 'password2' in self.fields:
            self.fields['password2'].help_text = None

    def clean_username(self):
        """Valide qu'un nom d'utilisateur identique n'existe pas (insensible à la casse)."""
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà utilisé. Veuillez en choisir un autre.")
        return username

    

# --- Formulaire 2 : Mise à jour de l'utilisateur ---
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        # 1. Appel au bon parent (UserUpdateForm)
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        
        # 2. Modification des champs, un par un
        self.fields['username'].help_text = ""
        self.fields['email'].help_text = ""

# --- Formulaire 3 : Mise à jour du profil ---
# Celui-ci était déjà correct.
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = profileModel
        fields = ['image']

        