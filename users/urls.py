from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/",views.users_login_view,name="login"),
    path("register/",views.users_register_view,name="register"),
    path("logout/",views.users_logout_view,name="logout")
]
