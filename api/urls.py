from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('uchwaly', views.UchwalaViewSet, basename='uchwaly')
router.register('users', views.MieszkaniecViewSet)
router.register('spotkania', views.HarmonogramViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('update-contact-info/', views.UpdateContactInfoView.as_view(), name='update_contact_info'),

    path('usterki/', views.UsterkaListCreateView.as_view(), name='usterki-list-create'),

    # Ścieżki dla administratorów
    path('usterki/admin/', views.UsterkaAdminView.as_view(), name='usterki-admin-list'),
    path('usterki/admin/<int:id>/', views.UsterkaAdminViewDetail.as_view(), name='usterki-admin-detail'),

    # Ścieżki dla admina (Rozliczenie)
    path('rozliczenia/admin/', views.RozliczenieAdminView.as_view()),
    path('rozliczenia/admin/<int:id>/', views.RozliczenieAdminViewDetail.as_view()),

    # Ścieżki dla mieszkańca (Rozliczenie)
    path('rozliczenia/mieszkaniec/', views.RozliczenieMieszkaniecView.as_view()),
    path('rozliczenia/mieszkaniec/<int:id>/', views.RozliczenieMieszkaniecView.as_view()),

    # Ścieżki dla admina (liczniki)
    path('liczniki/admin/', views.LicznikAdminView.as_view(), name='liczniki-admin-list'),
    path('liczniki/admin/<int:id>/', views.LicznikAdminViewDetail.as_view(), name='liczniki-admin-detail'),

    # Ścieżki dla mieszkańca (liczniki)
    path('liczniki/mieszkaniec/', views.LicznikMieszkaniecView.as_view(), name='liczniki-mieszkaniec-list'),
    path('liczniki/mieszkaniec/<int:id>/', views.LicznikMieszkaniecView.as_view(), name='liczniki-mieszkaniec-detail'),

    path('login/', views.LoginView.as_view(), name='custom_login'),

]