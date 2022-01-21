from django.urls import path
from .views import Index, NewsDetailView, SearchVideo, SearchFilm, VideoDetaillView, FilterCategory, AIView

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('news/<slug:slug>', NewsDetailView.as_view(), name='news_detail'),
    path('search/', SearchFilm.as_view(), name='search_news'),
    path('video-detail/<slug:slug>', VideoDetaillView.as_view(), name='video_detail'),
    path('search/', SearchVideo.as_view(), name='search_video'),
    path('filtercategory/', FilterCategory.as_view(), name='filter_category'),
    path('demonstration', AIView.as_view(), name='ai_view'),
]