from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('env/<str:env_name>/', views.detail, name='detail'),
    path('registered', views.registred, name='registered'),
    path('registered/<str:env_name>/', views.registred, name='registered_show_detail'),
    path('registered/<str:env_name>/<str:action>', views.registred, name='reload_registered'),
    path('loaded', views.loaded, name='loaded'),
    path('loaded/<str:env_name>/', views.loaded, name='loaded_show_detail')
]
