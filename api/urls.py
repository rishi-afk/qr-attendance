from django.urls import path
from api import views

urlpatterns = [
    path('entry/', views.entry),
    path('exit/', views.exit),
]
