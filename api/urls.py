from django.urls import path
from . import views

urlpatterns = [
    path("uchwaly/", views.UchwalaList.as_view()),
    path("uchwaly/<int:id>/", views.UchwalaDetails.as_view()),
]