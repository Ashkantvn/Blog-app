from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("",views.users_view,name="info"),
    path("login/",views.users_login_view,name="login"),
    path("register/",views.users_register_view,name="register"),
    path("logout/",views.users_logout_view,name="logout"),
    path("change",views.users_change_pass_view,name="change-pass"),
]
