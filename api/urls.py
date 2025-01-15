from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('uchwaly', views.UchwalaViewSet, basename='uchwaly')
router.register('users', views.MieszkaniecViewSet)
router.register('spotkania', views.HarmonogramViewSet)
router.register('liczniki', views.LicznikViewSet)
router.register('rozliczenia', views.RozliczeniaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('update-contact-info/', views.UpdateContactInfoView.as_view(), name='update_contact_info'),
    path('usterki/', views.UsterkaListCreateView.as_view(), name='usterki-list-create'),
    path('usterki/admin/', views.UsterkaAdminView.as_view(), name='usterki-admin-list'),
    path('usterki/admin/<int:pk>/', views.UsterkaAdminView.as_view(), name='usterki-admin-detail'),
    path('user-info/', views.getUserInfo, name='user-info'),  # Add this line
    path('login/', views.login, name='login'),
    path('stworz-mieszkanca/', views.CreateMieszkaniecView.as_view(), name='create_mieszkaniec'),
]