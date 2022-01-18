from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from .models import News, Reviews, Category


class Categor:
    """Жанры и года выхода фильмов"""
    def get_category(self):
        return Category.objects.all()

class Index(Categor, ListView):
    #Домашняя страница, список новостей
    model = News
    queryset = News.objects.all()
    template_name = 'reviews_ali/index.html'

class NewsDetailView(Categor,DetailView):
    model = News
    slug_field = 'url'
    template_name = 'reviews_ali/news_detail.html'

class SearchFilm(Categor,ListView):
    template_name = 'reviews_ali/index.html'

    def get_queryset(self):
        return News.objects.filter(title__icontains=self.request.GET.get('search_news'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search_news'] = f'searchnews={self.request.GET.get("search_news")}&'
        return context

class VideoView(Categor, ListView):
    model = Reviews
    queryset = Reviews.objects.all()
    template_name = 'reviews_ali/artificial_dme.html'


class VideoDetaillView(Categor, DetailView):
    model = Reviews
    slug_field = 'url'
    template_name = 'reviews_ali/video_detail.html'


class SearchVideo(Categor, ListView):
    template_name = 'reviews_ali/artificial_dme.html'

    def get_queryset(self):
        return Reviews.objects.filter(title__icontains=self.request.GET.get('search_video'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search_video'] = f'searchvideo={self.request.GET.get("search_video")}&'
        return context

class FilterCategory(Categor, ListView):
    template_name = 'reviews_ali/filtercategory.html'

    def get_queryset(self):
        queryset = 0
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['videos'] = Reviews.objects.filter(
            category__in=self.request.GET.getlist('category')
        )

        context['newss'] = News.objects.filter(
            category_news__in=self.request.GET.get('category')
        )
        return context


