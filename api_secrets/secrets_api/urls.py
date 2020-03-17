from django.urls import path

from . import views

urlpatterns = [
    path('<str:env_name>/', views.get_secrets, name='get_secrets'),
    path('', views.post_secrets, name='post_secrets')

]