from django.contrib import admin

from feedback.models import Author, Feedback, StatusLog

__all__ = []


class AuthorInline(admin.TabularInline):
    model = Author
    can_delete = False


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        Feedback.text.field.name,
        Feedback.status.field.name,
    )

    inlines = (AuthorInline,)

    def save_model(self, request, obj, form, change):
        old_obj = self.model.objects.get(id=obj.id)
        if old_obj.status != obj.status:
            StatusLog.objects.create(
                user=request.user,
                from_status=old_obj.status,
                to=obj.status,
            )
        super().save_model(request, obj, form, change)
