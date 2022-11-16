from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import context
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from . import models

base_context =  {
        "popular_tags": models.POPULAR_TAGS,
        "best_members": models.BEST_MEMBERS,
        }

def index(request) :
   return render(request, 'index.html', context=(base_context | paginate(models.QUESTIONS, request))) 

def login(request) :
    return render(request, 'login.html', context=base_context)

def signup(request) :
    return render(request, 'signup.html', context=base_context)

def ask(request) :
    return render(request, 'ask.html', context=base_context)

def question(request, id: int) :
    if id >= len(models.QUESTIONS) :
        return render(request, "page404.html", status=404)
    question_item = models.QUESTIONS[id]
    context = {"question": question_item} | paginate(question_item.get("answers"), request) 
    return render(request, 'question.html', context=(context | base_context))

def tag_page(request, tag_name: str) :
    if tag_name not in models.TAGS:
        return render(request, "page404.html", status=404)
    context = {"tag": tag_name} | paginate(models.QUESTIONS, request)
    return render(request, "tag.html", context=(context | base_context)) 

def hot(request) :
    return render(request, 'hot.html', context=(base_context | paginate(models.HOT_QUESTIONS, request)))

def paginate(objects_list, request, per_page=20):
   paginator = Paginator(objects_list, per_page)
   page_number = request.GET.get("page") or 1
   try : 
        page_obj = paginator.get_page(page_number)
   except :
        page_obj = paginator.get_page(1)
        page_number = 1
   return  {
                "elided_page_range": paginator.get_elided_page_range(number=page_number, on_each_side=2, on_ends=1),
                "page_obj": page_obj,
                "ELLIPSIS": paginator.ELLIPSIS,
            }
 



