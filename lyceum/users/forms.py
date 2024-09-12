from django import forms
from django.contrib.auth.models import User

from users.models import Profile

__all__ = []


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = User
        fields = [
            User.first_name.field.name,
            User.last_name.field.name,
            User.email.field.name,
        ]


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Profile
        fields = [
            Profile.birthday.field.name,
            Profile.image.field.name,
        ]
