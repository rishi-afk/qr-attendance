from django.urls import path
from dashboard import views
from django.contrib.auth import views as auth_views
from .views import attendance


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html",
                                                redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("attendance/<int:paper_id>/", attendance, name="attendance"),
]
