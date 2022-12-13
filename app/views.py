from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from . import models

base_context = {
    "popular_tags": models.Tag.objects.all()[:6],
    "best_members": models.Profile.objects.all()[:5],
}


def index(request):
    return render(
        request,
        'index.html',
        context=(
            base_context | paginate(
                models.Question.objects.order_by_date(),
                request)))


def login(request):
    return render(request, 'login.html', context=base_context)


def signup(request):
    return render(request, 'signup.html', context=base_context)


def ask(request):
    return render(request, 'ask.html', context=base_context)


def question(request, id: int):
    question_item = models.Question.objects.get_by_id(id)
    context = {"question": question_item} | paginate(
        models.Answer.objects.get_answers(question_item), request, per_page=10)
    return render(request, 'question.html', context=(context | base_context))


def tag_page(request, tag_name: str):
    context = {"tag": tag_name} | paginate(
        models.Question.objects.get_by_tag(tag_name), request)
    return render(request, "tag.html", context=(context | base_context))


def hot(request):
    return render(
        request,
        'hot.html',
        context=(
            base_context | paginate(
                models.Question.objects.order_by_rating(),
                request)))


def paginate(objects_list, request, per_page=20):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get("page") or 1
    page_obj = paginator.get_page(page_number)
    result = {
        "page_obj": page_obj,
        "ELLIPSIS": paginator.ELLIPSIS,
        "elided_page_range": []
    }
    try:
        result["elided_page_range"] = [
            p for p in paginator.get_elided_page_range(
                number=page_number, on_each_side=2, on_ends=1)]
    except (PageNotAnInteger, EmptyPage):
        result["elided_page_range"] = [
            p for p in paginator.get_elided_page_range(
                number=paginator.num_pages, on_each_side=2, on_ends=1)]
    return result
