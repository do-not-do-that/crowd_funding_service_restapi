from django.urls import path, include
from . import views

app_name = "users"

urlpatterns = [
    path('signup/', views.UserCreate.as_view()),
 ]
