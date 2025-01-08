from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/<str:user_name>/", views.room, name="room"),
    path('createroom/', views.ProtectedView.as_view()),
    path('getchats/<str:username>', views.ChatUsers.as_view()),
    path('changeadmin/', views.ChangeAdmin.as_view()),
    path('changeclose/', views.ChangeClose.as_view()),
    path('usermessagescount/<str:username>', views.UserMessagesCount.as_view()),
    path('upload/', views.FileUploadView.as_view(), name='file-upload'),
]