from django.conf.urls import include, url
from django.contrib.auth.views import logout

from .views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'', include('social_django.urls')),
    url(r'^logout/$', logout, name='logout'),
]
