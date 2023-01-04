from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.without, name='without'),
    path('mine', views.mine, name='mine'),
    path('ready', views.ready, name='ready'),
    path('tips', views.tips, name='tips'),
    path('withoutstart', views.withoutstart, name='withoutstart'),
    path('withoutstop', views.withoutstop, name='withoutstop'),
    path('start', views.start, name='start'),
    path('stop', views.stop, name='stop'),
    path('play', views.play, name='play'),
    path('advices', views.advices, name='advices'),
]
