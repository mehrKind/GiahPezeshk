from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/<str:user_name>/", views.room, name="room"),
    path('createroom/', views.ProtectedView.as_view()),
    path('getchats/<str:username>', views.ChatUsers.as_view()),
]