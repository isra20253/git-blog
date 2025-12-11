# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostModelForm, postUpdateform, commentForm
from .models import postModel
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden # <-- NOUVEAU : On importe la réponse "Accès Interdit"

@login_required
def index(request):
    # Si on envoie le formulaire (POST)
    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user # On assigne l'auteur manuellement
            instance.save()
            return redirect('blog-index')
    # Si on affiche la page (GET)
    else:
        form = PostModelForm()

    posts = postModel.objects.all()
    
    context = {
        'posts': posts,
        'form': form
    }
    return render(request, 'index.html', context)

@login_required
def post_detail(request, pk):
    # Utilise get_object_or_404 pour renvoyer une 404 propre
    # au lieu d'une exception 500 si l'objet n'existe pas.
    post = get_object_or_404(postModel, id=pk)
    if request.method == "POST":
        # Gestion d'envoi de commentaire : on attache l'utilisateur
        # et le post avant de sauvegarder pour éviter les données orphelines.
        c_form = commentForm(request.POST)
        if c_form.is_valid():
            comment_instance = c_form.save(commit=False)
            comment_instance.post = post
            comment_instance.user = request.user
            comment_instance.save()
            return redirect('blog-post_detail', pk=post.id)
    else:   
        c_form = commentForm()      
    context = {
        'post': post,
        'c_form': c_form
    }
    return render(request, 'post_detail.html', context)

@login_required
def post_edit(request, pk):
    post = get_object_or_404(postModel, id=pk)
    
    # ==================== VÉRIFICATION DE SÉCURITÉ AJOUTÉE ICI ====================
    # On vérifie si l'utilisateur qui fait la requête est bien l'auteur du post.
    if request.user != post.author:
        # Si ce n'est pas le cas, on lui refuse l'accès.
        return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier ce post.")
    # ========================== FIN DE LA VÉRIFICATION ==========================

    if request.method == 'POST':
        form = postUpdateform(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog-post_detail', pk=post.id)
    else:
        form = postUpdateform(instance=post)
    
    context = {
        'form': form,
        'post': post
    }
    return render(request, 'post_edit.html', context)

@login_required
def post_delete(request, pk):
    post = get_object_or_404(postModel, id=pk)

    # ==================== VÉRIFICATION DE SÉCURITÉ AJOUTÉE ICI ====================
    # On vérifie également ici avant de permettre la suppression.
    if request.user != post.author:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer ce post.")
    # ========================== FIN DE LA VÉRIFICATION ==========================

    if request.method == 'POST':
        post.delete()
        return redirect('blog-index')
    
    context = {
        'post': post
    }
    # Utiliser le template présent dans `blog/templates/post_delete.html`
    # (le nom `blog-post_delete.html` n'existait pas, provoquant
    # TemplateDoesNotExist). On rend désormais le template correct.
    return render(request, 'post_delete.html', context)