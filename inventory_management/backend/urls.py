from django.urls import path

from .views import UserVisit, CharacterInventory

app_name = "backend"

urlpatterns = [
    path("users/", UserVisit.as_view()),
    path("inventory/", CharacterInventory.as_view()),
]