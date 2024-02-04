from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(
        max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(
        max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = models.SlugField(unique=True)

    def clean(self):
        """Django Framework expects the url field to be corractly formatted, and complete URL paths."""
        # obtained from the ModelForm dictionary attribute cleaned_data
        cleaned_data = self.cleaned_data
        # form fields to be checked taken from the cleaned_data dictionary
        url = cleaned_data.get('url')
        # if empty and does not start with 'http://'
        if url and not url.startswith('http://'):
            url = f'http://{url}'   # prepend the link
            cleaned_data['url'] = url  # clean it recursively
        return cleaned_data

    class Meta:
        model = Page
        # some fields allow NULL values; here ForeignKeys are hidden
        exclude = ('category',)  # excluding the category field from the form
        # we could specify the filed to include - fields = ('title', 'url', 'views')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)
