import datetime

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render, reverse

from users.models import Profile, User
from users.forms import ProfileForm, UserForm

__all__ = []


def register(request):
    template = "users/signup.html"
    register_form = UserCreationForm(request.POST or None)

    if request.method == "POST" and register_form.is_valid():
        user = register_form.save(commit=False)
        user.is_active = settings.DEFAULT_USER_IS_ACTIVE
        user.save()
        Profile.objects.create(user=user)
        login(request, user)
        return redirect(reverse("homepage:home"))
    context = {
        "register_form": register_form,
    }
    return render(request, template, context)


def activate(request, username):
    template = "users/activate.html"
    user = User.objects.get(username=username)
    difference_time = datetime.datetime.today() - user.date_joined
    is_accept = difference_time < datetime.timedelta(hours=12)
    if is_accept:
        user.is_active = True
        user.save()
        login(request, user)
    context = {"is_accept": is_accept}
    return render(request, template, context)


def user_list(request):
    template = "users/user_list.html"
    users = (
        Profile.objects.filter(user__is_active=True).select_related("user").only(
            Profile.image.field.name,
            f"{Profile.user.field.name}__{User.email.field.name}",
            f"{Profile.user.field.name}__{User.username.field.name}",
        )
    )
    context = {"users": users}
    return render(request, template, context)


def user_detail(request, user_id):
    template = "users/user_detail.html"
    user = get_object_or_404(
        Profile.objects.select_related('user').only(
            Profile.coffee_count.field.name,
            Profile.image.field.name,
            Profile.birthday.field.name,
            f"{Profile.user.field.name}__{User.email.field.name}",
            f"{Profile.user.field.name}__{User.last_name.field.name}",
            f"{Profile.user.field.name}__{User.first_name.field.name}",
        ), user__id=user_id,
    )
    context = {"user_profile": user}
    return render(request, template, context)


@login_required
def profile(request):
    template = "users/profile.html"
    profile = get_object_or_404(
        Profile.objects.select_related('user').only(
            Profile.coffee_count.field.name,
            Profile.image.field.name,
            Profile.birthday.field.name,
            f"{Profile.user.field.name}__{User.email.field.name}",
            f"{Profile.user.field.name}__{User.last_name.field.name}",
            f"{Profile.user.field.name}__{User.first_name.field.name}",
        ), user__id=request.user.id,
    )
    user_form = UserForm(request.POST or None, instance=profile.user)
    profile_form = ProfileForm(request.POST or None,
                               request.FILES or None,
                               instance=profile)
    if request.method == 'POST' and (user_form.is_valid() and profile_form.is_valid()):
        user_form.save()
        profile_form.save()
        return redirect(reverse("users:profile"))

    context = {"user_form": user_form,
               "profile_form": profile_form, }
    return render(request, template, context)
