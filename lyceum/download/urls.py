from django.urls import path

from download import views

app_name = "download"

urlpatterns = [
    path("<path:image_url>/", views.download_file, name="download"),
]
