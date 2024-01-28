import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page


def populate():
    ''' First create lists of dictionaries containing the pages we want ot add into each category.
        Then create a dictionary of dictionaries for the categories.
        It allows to iterate thorugh each data structure, and add teh data to our models.'''

    python_pages = [
        {'title': 'Official Python Tutorial',
         'url': 'http://docs.python.org/3/tutorial/', 'views': 209},
        {'title': 'How to Think like a Computer Scientist',
         'url': 'http://www.greenteapress.com/thinkpython/', 'views': 110},
        {'title': 'Learn Python in 10 Minutes',
         'url': 'http://www.korokithakis.net/tutorials/python/', 'views': 909}]

    django_pages = [
        {'title': 'Official Django Tutorial',
         'url': 'https://docs.djangoproject.com/en/2.1/intro/tutorial01/', 'views': 125},
        {'title': 'Django Rocks',
         'url': 'http://www.djangorocks.com/', 'views': 87},
        {'title': 'How to Tango with Django',
         'url': 'http://www.tangowithdjango.com/', 'views': 44}]

    other_pages = [
        {'title': 'Bottle',
         'url': 'http://bottlepy.org/docs/dev/', 'views': 578},
        {'title': 'Flask',
         'url': 'http://flask.pocoo.org', 'views': 112}]

    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
            'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
            'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16}}

    # You can add more categories or pages to the dictionaries above.

    """The code below goes through the cats dictionary, then adds each category, and then
        adds all associated pages for that category."""
    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])

    # Print out the categories added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')


def add_page(cat, title, url, views=0):
    p, created = Page.objects.get_or_create(category=cat, title=title)
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name, views=0, likes=0):
    c, created = Category.objects.get_or_create(name=name)
    c.views = views
    c.likes = likes
    c.save()  # the slug should have been generated here
    return c


# Executing the main function
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
