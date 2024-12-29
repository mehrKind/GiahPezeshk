from django.urls import path
from . import views


urlpatterns = [
    path("daily_text/", views.DailyTextView.as_view()),
]

