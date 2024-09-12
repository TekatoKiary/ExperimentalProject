from http import HTTPStatus

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from catalog.models import Item
from homepage.forms import EchoForm
from users.models import Profile

__all__ = []


def home(request):
    template = "homepage/main.html"
    item_list = Item.objects.on_main()
    context = {"items": item_list}
    return render(request, template, context)


def coffee(request):
    if Profile.objects.filter(user__id=request.user.id).exists():
        user = Profile.objects.get(user__id=request.user.id)
        user.coffee_count += 1
        user.save()
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


@require_GET
def echo(request):
    template = "homepage/echo.html"
    context = {"echo_form": EchoForm()}
    return render(request, template, context)


@require_POST
def echo_submit(request):
    form = EchoForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data.get("text")
        return HttpResponse(
            text,
            content_type="text/plain; charset=utf-8",
        )
    return HttpResponseBadRequest("Неправильная форма")
