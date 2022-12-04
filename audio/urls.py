from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.without, name='without'),
    path('mine', views.mine, name='mine'),
    path('ready', views.ready, name='ready'),
    path('tips', views.tips, name='tips')
]
