from django.conf.urls import url
from . import views

app_name = 'rango'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.abount, name='about'),
    url(r'^category/(?P<slug>[\w\-]+)/$', views.CategoryDetailView.as_view(), name='show_category'),
    url(r'^add_category/$', views.add_category, name='add_category',),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^goto/$', views.track_url, name='goto'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^profile/(?P<pk>\d+)/$', views.ProfileDetailView.as_view(), name='profile'),
    url(r'^edit_profile/(?P<username>[\w\-]+)/$', views.update_profile, name='edit_profile'),
    url(r'^profiles/$', views.ListProfiles.as_view(), name='profiles'),
    url(r'^like/$', views.like_category, name='likes'),
    url(r'^suggest/$', views.suggest_category, name='suggestion'),
]