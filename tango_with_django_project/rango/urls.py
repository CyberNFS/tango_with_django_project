from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),

    path('category/<slug:category_name_slug>/',
         views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),


    path('category/<slug:category_name_slug>/add_page/',
         views.add_page, name='add_page'),

    # tutorial 3
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # tutorial 4
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # Chapter 9
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),


]
