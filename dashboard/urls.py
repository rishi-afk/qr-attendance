from django.urls import path
from dashboard import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html",
                                                redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("change-password/", auth_views.PasswordChangeView.as_view(template_name='auth/change_password.html', success_url="/"),
         name="change-password"),
    path("register/", views.register, name="register")
]
