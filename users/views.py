from django.shortcuts import render, redirect 
from django.contrib.auth import logout
from .forms import signUpForm, UserUpdateForm , ProfileUpdateForm    # Assure-toi que la classe s'appelle bien signUpForm dans forms.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import profileModel




def log_out(request):
    logout(request) # Déconnecte l'utilisateur
    return render(request, 'users/logout.html')

def sign_up(request):
    if request.method == 'POST':
        form = signUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog-index') 
    else:
        form = signUpForm()
    
    context = {
        'form': form
    }    
    return render(request, 'users/sign_up.html', context)


@login_required
def profile(request):
    # On s'assure qu'un `profile` existe pour l'utilisateur courant.
    # get_or_create évite l'exception RelatedObjectDoesNotExist lorsque
    # l'utilisateur n'a pas encore de profile lié (par ex. utilisateurs
    # créés avant l'ajout du signal). Cela permet d'instancier le
    # ProfileUpdateForm sans erreur.
    profile_obj, created = profileModel.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # On utilise explicitement l'instance `profile_obj` retournée ci-dessus
        # pour remplir le formulaire de profil. Ainsi, même si le profile a
        # été créé à la volée, le formulaire cible la bonne instance.
        u_form = UserUpdateForm(request.POST or None, instance=request.user)
        p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile_obj)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f'Your account has been updated!')    
            return redirect('users-profile')

    else:
        # En GET on instancie les formulaires avec les instances existantes
        # (user + profile). Grâce à get_or_create, profile_obj est garanti.
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile_obj)

    context = {
        'u_form': u_form,
        'p_form': p_form        
    }
    return render(request, 'users/profile.html', context)