from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.without, name='without'),
    path('minetext', views.minetext, name='minetext'),
    path('readytext', views.readytext, name='readytext'),
    path('tips', views.tips, name='tips')
]
