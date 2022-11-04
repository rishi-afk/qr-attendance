from django.urls import path
from .views import entry, exit

urlpatterns = [
    path("entry/", entry, name="entry"),
    path("exit/", exit, name="exit"),
]
