from django.urls import path, include
from . import views
# from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView
# )

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path("me/", views.UserProfileView.as_view()),
    path("password_recovery/", views.PasswordRecoveryViewSet.as_view()),
    path("change_password/", views.ChangePasswordView.as_view()),
    path("all_users/", views.AllUserProfilesView.as_view(), name="all_users"),
    path("all_specialist/", views.AllSpecialistView.as_view()),
    path("add_specialist/", views.AdminRegisterView.as_view()),
    path("me_update_admin/", views.SelfAdminUpdateProfile.as_view()),
    path("me_update", views.UserProfileUpdateView.as_view()),
    path("register/", views.RegisterView.as_view()),
    path('delete_user/<int:user_id>/', views.UserDeleteView.as_view(),),
    path("logout/", views.LogoutView.as_view(), name="logout")
]

