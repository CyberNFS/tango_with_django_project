from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Category, Page, Question, Choice
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from datetime import datetime


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

    # Chapter 10
    visitor_cookie_handler(request)
    # context_dict['visits'] = request.session['visits']
    request.session.set_test_cookie()
    response = render(request, 'rango/index.html', context=context_dict)
    return response


def about(request):
    # index_url = reverse('rango:index')
    # return HttpResponse(f"Rango says here is the about page. \
    #                     <a href='{index_url}'>Index</a>")

    print(request.method)
    print(request.user)

    # Chapter 10
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()

    visitor_cookie_handler(request)
    context_dict = {'visits': request.session['visits']}

    return render(request, 'rango/about.html', context=context_dict)


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


@login_required
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


@login_required
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


# Chapter 9
def register(request):
    registered = False  # True when registration succeeds
    # POST request
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        # Validity CHECK
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            # Profile picture check
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True   # Registration was successfull
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def user_login(request):
    # POST request
    if request.method == 'POST':
        # POST.get – returns None if value doesn't exist
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        # Check for validity
        if user:
            if user.is_active:
                # if valid and active, login and redirect to homepage
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")

        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    # not a 'POST' request so display the login form
    else:
        return render(request, 'rango/login.html')


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


# Chapter 10
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(
        request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(
        last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    # Condition - it's been more than a day since the last visit
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        # Update the last visit cookie
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Set the visits cookie
    request.session['visits'] = visits


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val
