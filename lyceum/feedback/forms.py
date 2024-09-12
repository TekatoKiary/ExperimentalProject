from django import forms

from feedback.models import Author, Feedback, FeedbackFile

__all__ = []


class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Feedback
        fields = [
            Feedback.text.field.name,
        ]
        exclude = [Feedback.created_on.field.name, Feedback.status.field.name]


class AuthorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Author
        fields = [
            Author.name.field.name,
            Author.mail.field.name,
        ]


class FileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
        self.fields["file"].widget.attrs["multiple"] = True

    class Meta:
        model = FeedbackFile

        fields = [FeedbackFile.file.field.name]
