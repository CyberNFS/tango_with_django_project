from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from rango.models import Category, Page


def index(request):
    # about_url = reverse('rango:about')
    # return HttpResponse(f"Rango says hey there partner! \
    #                     <a href='{about_url}'>About</a>")

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
                    'categories': category_list}

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
