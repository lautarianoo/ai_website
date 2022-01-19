from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Reviews, News, ImageAI


from ckeditor_uploader.widgets import CKEditorUploadingWidget

admin.site.register(ImageAI)
class ReviewsAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    video = forms.CharField(label="Видео", widget=CKEditorUploadingWidget())

    class Meta:
        model = Reviews
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "title", "url")
    list_display_links = ("title",)







    readonly_fields = ('get_poster',)

    def get_poster(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="60">')

    def unpublish(self, request, queryset):
        '''Снять с публикации(action)'''
        row_update = queryset.update()
        if row_update == 1:
            message_bit = '1 запис было объявлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        '''Опубликолвать(action)'''
        row_update = queryset.update()
        if row_update == 1:
            message_bit = '1 запис было объявлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)

    get_poster.short_description = 'Превью'




@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    '''Новости'''
    list_display = ('title', 'category_news', 'url', 'date', 'get_image',)
    list_filter = ('category_news', 'date',)
    search_fields = ('title', 'category_news__title',)
    form = ReviewsAdminForm
    actions = ['publish', 'unpublish']

    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    def unpublish(self, request, queryset):
        '''Снять с публикации(action)'''
        row_update = queryset.update()
        if row_update == 1:
            message_bit = '1 запис было объявлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        '''Опубликолвать(action)'''
        row_update = queryset.update()
        if row_update == 1:
            message_bit = '1 запис было объявлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = 'Превью'

class AliAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ('title', 'url', 'price', 'get_poster',)
    list_filter = ('price', 'title',)
    search_fields = ('title', 'price',)
    #inlines = [FeedbackInline]
    form = ReviewsAdminForm
    actions = ['publish', 'unpublish']

    readonly_fields = ('get_poster',)

    def get_poster(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="60">')

    def unpublish(self, request, queryset):
        '''Снять с публикации(action)'''
        row_update = queryset.update()
        if row_update == 1:
            message_bit = '1 запис было объявлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        '''Опубликолвать(action)'''
        row_update = queryset.update()
        if row_update == 1:
            message_bit = '1 запис было объявлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)

    get_poster.short_description = 'Превью'

admin.site.site_title = "Techno Website"
admin.site.site_header = "Techno Website"

