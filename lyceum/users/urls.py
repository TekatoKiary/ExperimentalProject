from django.contrib.auth import views
from django.urls import path

from users.views import activate, profile, register, user_detail, user_list

app_name = "users"

urlpatterns = [
    path(
        "login/",
        views.LoginView.as_view(
            template_name="users/login.html",
        ),
        name="login",
    ),
    path(
        "logout/",
        views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "password_change/",
        views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uid64>/<token>",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(
            template_name="users/reset_done.html",
        ),
        name="reset_done",
    ),
    path("register/", register, name="register"),
    path("activate/<username>/", activate, name="activate"),
    path("users/user_list/", user_list, name="user_list"),
    path("users/user_detail/<int:user_id>/", user_detail, name="user_detail"),
    path("users/profile/", profile, name="profile"),
]
