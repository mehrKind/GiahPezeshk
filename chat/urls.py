from django.urls import path
from .views import MessageHistoryView

urlpatterns = [
    path('api/messages/<str:room_name>/', MessageHistoryView.as_view(), name='message_history'),
]
