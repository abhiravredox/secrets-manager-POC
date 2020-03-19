from django.urls import path

from . import views

urlpatterns = [
    path('', views.registred, name='registered'),
    path('<str:env_name>', views.registred, name='registered_show_detail'),
    path('reload/<str:env_name>/', views.reload_registered, name='reload_registered'),
    path('deployed/', views.deployed, name='deployed'),
    path('reload_deployed/', views.reload_deployed, name='reload_deployed'),
]
