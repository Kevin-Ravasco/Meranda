from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.searchposts, name='search_results'),
    path('trending/', views.trending, name='trending'),
    path('popular/', views.popular, name='popular'),
    path('<str:name>/', views.category, name='category'),
    path('<str:name>/<slug:slug>/', views.blog_single, name='blog_single'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)