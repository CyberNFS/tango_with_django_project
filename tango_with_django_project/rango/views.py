from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from rango.models import Category, Page, Question


def index(request):
    # about_url = reverse('rango:about')
    # return HttpResponse(f"Rango says hey there partner! \
    #                     <a href='{about_url}'>About</a>")

    category_list = Category.objects.order_by(
        '-likes')[:5]  # descending order top5
    page_list = Page.objects.order_by('-views')[:5]  # descending order top5
    latest_question_list = Question.objects.order_by(
        '-pub_date')[:5]  # desecnding order top5
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
                    'categories': category_list, 'pages': page_list, 'latest_questions': latest_question_list}

    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    # index_url = reverse('rango:index')
    # return HttpResponse(f"Rango says here is the about page. \
    #                     <a href='{index_url}'>Index</a>")

    return render(request, 'rango/about.html')


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)


# tutorial 3
def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    question = get_object_or_404(Question, id=question_id) # id could be replaced by pk
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
