from django import template
from reviews_ali.models import Category, News

register = template.Library()

@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()

@register.inclusion_tag('reviews_ali/tags/last_news.html')
def get_last_movies(count=5):
    '''Вывод последних фильмов'''
    movies = News.objects.order_by('-id')[:count]
    return {'last_movie': movies}