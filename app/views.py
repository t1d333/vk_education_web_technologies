from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.contrib import auth
from . import models, forms

base_context = {
    "popular_tags": models.Tag.objects.all()[:6],
    "best_members": models.Profile.objects.all()[:5],
}


def logout(request: HttpRequest):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def index(request: HttpRequest):
    return render(
        request,
        'index.html',
        context=(
            base_context | paginate(
                models.Question.objects.order_by_date(),
                request)))


def login(request: HttpRequest):
    if request.method == 'GET':
        login_form = forms.LoginForm()
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(request.GET.get('continue'))
            else:
                login_form.add_error('username', '')
                login_form.add_error('password', '')
                login_form.add_error(
                    field=None, error="The login or password is incorrect.")

    return render(
        request,
        'login.html',
        context=base_context | {
            'form': login_form})


def signup(request: HttpRequest):
    if request.method == 'GET':
        register_form = forms.RegisterForm()
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            user = auth.authenticate(request, **user)
            auth.login(request, user)
            return HttpResponseRedirect("/")

    return render(
        request,
        'signup.html',
        context=base_context | {
            "form": register_form})


def ask(request: HttpRequest):
    if request.method == 'GET':
        ask_form = forms.QuestionForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            ask_form = forms.QuestionForm(request.POST)
            if ask_form.is_valid():
                question = ask_form.save(request.user.get_username())
                return HttpResponseRedirect(f'/question/{question.pk}')
        else:
            return HttpResponseRedirect("/login?continue=/ask")
    return render(request, 'ask.html', context=base_context | {'form': ask_form})


def question(request: HttpRequest, id: int):

    question_item = models.Question.objects.get_by_id(id)
    if request.method == 'GET':
        answer_form = forms.AnswerForm()
        print(123)
    if request.method == 'POST':
        if request.user.is_authenticated:
            answer_form = forms.AnswerForm(request.POST)
            if answer_form.is_valid():
                answer = answer_form.save(request)
                return HttpResponseRedirect(request.path + "#answer-" + str(answer.pk))
        else:
            return HttpResponseRedirect("/login?continue=/ask")
    context = {"question": question_item} | paginate(models.Answer.objects.get_answers(question_item) , request, per_page=10) | {'form': answer_form}
    return render(request, 'question.html', context=(context | base_context))


def tag_page(request: HttpRequest, tag_name: str):
    context = {"tag": tag_name} | paginate(
        models.Question.objects.get_by_tag(tag_name), request)
    return render(request, "tag.html", context=(context | base_context))


def hot(request: HttpRequest):
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
