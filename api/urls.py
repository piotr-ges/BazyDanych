from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('uchwaly', views.UchwalaViewSet, basename='uchwaly')
router.register('users', views.MieszkaniecViewSet)

urlpatterns = [
    path('', include(router.urls)),

]