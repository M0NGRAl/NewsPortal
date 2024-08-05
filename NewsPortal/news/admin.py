from django.contrib import admin
from .models import Post, PostCategory, Author, Category, Comment

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Author)
admin.site.register(Comment)

class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = [field.name for field in Post._meta.get_fields()] # генерируем список имён всех полей для более красивого отображения