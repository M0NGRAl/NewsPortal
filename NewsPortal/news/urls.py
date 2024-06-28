from django.urls import path
# Импортируем созданные нами представления
from .views import *

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('posts/', PostsList.as_view(), name='posts_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('post/<int:pk>/', PostDetail.as_view(), name='posts_detail'),
   path('news/create/', NewsCreate.as_view()),
   path('articles/create/', ArticleCreate.as_view()),
   path('news/<int:pk>/edit/', NewsEdit.as_view(), name='post_edit'),
   path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name='post_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view()),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view()),
   path('subscriptions/', subscriptions, name='subscriptions'),
   path('', IndexView.as_view()),

]