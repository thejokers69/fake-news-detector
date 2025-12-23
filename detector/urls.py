from django.urls import path
from . import views

app_name = "detector"

urlpatterns = [
    path("", views.home, name="home"),
    path("analyze/", views.analyze, name="analyze"),
    path("health/", views.health, name="health"),
]
