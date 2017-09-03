from django import forms
from django.contrib.auth.models import User

from rango.models import Category, Page, UserProfile


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text='Please enter the category name.')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name', )


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text='Please enter the title of page.')
    url = forms.URLField(max_length=200, help_text='Please enter the URL of page.')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category','last_visit', 'first_visit')

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserProfileForm(forms.ModelForm):
    # website = forms.URLField(required=False)
    # picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
        #exclude = ('user',)