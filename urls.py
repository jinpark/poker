from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView
from poker import views

urlpatterns = [
    url(r'^game_status/', views.game_status),
]
