from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='blog-index'),
    path('post_detail/<int:pk>/', views.post_detail, name='blog-post_detail'),
    path('post_edit/<int:pk>/', views.post_edit, name='blog-post_edit'),
     path('post_delete/<int:pk>/', views.post_delete, name='blog-post_delete')

]