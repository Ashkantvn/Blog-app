from django.urls import path
from accounts import views

app_name = "accounts"

urlpatterns = [
    # Authentication
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    # Account management
    path("profile/<str:user_slug>/", views.Profile.as_view(), name="profile"),
    path("update/", views.UpdateAccount.as_view(), name="update"),
    path("delete/", views.DeleteAccount.as_view(), name="delete"),
    # Reset and activation
    path("password-reset/", views.PasswordReset.as_view(), name="reset"),
    path(
        "password-reset/<str:code>/",
        views.PasswordResetConfirm.as_view(),
        name="reset-confirm",
    ),
    path(
        "activate/<str:user_slug>/",
        views.Activate.as_view(),
        name="activate"
    ),
]
