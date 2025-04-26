from django.urls import path
from .views import solr_search, home

urlpatterns = [
    path('', home),
    path('search/', solr_search, name='solr_search'),
]
