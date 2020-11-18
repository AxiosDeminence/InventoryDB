from django.urls import path

from .views import UserVisit, ItemManagement, CharacterManagement

app_name = "backend"

urlpatterns = [
    path("users/", UserVisit.as_view()),
    path("items/", ItemManagement.as_view()),
    path("characters/", CharacterManagement.as_view()),
]