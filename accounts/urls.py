from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path(f'login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("me/", views.UserProfileView.as_view()),
    path("password_recovery/", views.PasswordRecoveryViewSet.as_view()),
    path("change_password/", views.ChangePasswordView.as_view()),
    path("all_users/", views.AllUserProfilesView.as_view(), name="all_users"),
    path("all_specialist/", views.AllSpecialistView.as_view()),
    path("add_specialist/", views.AddSpecialistView.as_view()),
    path("register/", views.RegisterView.as_view()),
    path("logout/", views.LogoutView.as_view(), name="logout")
]

