from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from rango.models import Category, Page, Question, Choice
from rango.forms import CategoryForm, PageForm



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


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)   # HTTP - POST

        if form.is_valid():  # validity check
            form.save(commit=True)  # save to db

            return redirect('/rango/')  # confirm or redirect to index

        else:

            print(form.errors)  # the form had errors, print it out

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')
    form = PageForm()
    if request.method == 'POST':    # HTTP - POST
        form = PageForm(request.POST)
        if form.is_valid():   # similar validity check
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


# tutorial 3
def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # id could be replaced by pk
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'rango/detail.html', {'question': question})


# tutorial 4
def vote(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    try:
        # request.POST - data is only altered through a POST call
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question form
        return render(request, 'rango/detail.html', {'question': question, 'error_message': "You didn't select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # URL which the user will be redirected
        return HttpResponseRedirect(reverse('rango:results', args=(question.id,)))
    # return HttpResponse("You're voting on question %s." % question_id)

# tutorial 4
def results(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'rango/results.html', {'question': question})

# tutorial 4
class IndexView(generic.ListView):
    template_name = 'rango/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

# tutorial 4
class DetailView(generic.DetailView):
    model = Question
    template_name = 'rango/detail.html'

# tutorial 4
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'rango/results.html'


