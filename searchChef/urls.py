from django.urls import path
from searchChef import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.recipePage, name="recipe")
]
