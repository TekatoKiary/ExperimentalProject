from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render, reverse

from feedback.forms import AuthorForm, FeedbackForm, FileForm
from feedback.models import Author, Feedback, FeedbackFile

__all__ = []


def feedback(request):
    template = "feedback/feedback.html"
    feedback_form = FeedbackForm(request.POST or None)
    user_form = AuthorForm(request.POST or None)
    file_form = FileForm(
        request.POST or None,
    )
    if (
        request.method == "POST"
        and feedback_form.is_valid()
        and user_form.is_valid()
        and file_form.is_valid()
    ):
        name = user_form.cleaned_data.get("name")
        mail = user_form.cleaned_data.get("mail")
        text = feedback_form.cleaned_data.get("text")
        send_mail(
            name,
            text,
            None,
            [mail],
            fail_silently=False,
        )
        feedback_object = Feedback.objects.create(**feedback_form.cleaned_data)
        user_data = user_form.cleaned_data
        user_data["feedback"] = feedback_object
        Author.objects.create(**user_data)
        for file in request.FILES.getlist("file"):
            FeedbackFile.objects.create(file=file, feedback=feedback_object)

        messages.success(request, "Форма успешно отправлена")
        return redirect(reverse("feedback:feedback"))
    context = {
        "feedback_form": feedback_form,
        "user_form": user_form,
        "file_form": file_form,
    }
    return render(request, template, context, status=200)
