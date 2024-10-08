from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import datetime, timedelta
from django.urls import reverse_lazy
from .forms import *
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post
from .filters import NewsFilter
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import Subscription, Category
from django.utils.translation import gettext as _
from django.http import HttpResponse




class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'time_in'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10



    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['time_now'] = datetime.utcnow()
        return contex

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = ('post.html')
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    ordering = 'time_in'
    context_object_name = 'posts'


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.position = "news"
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'


    def form_valid(self, form):
        post = form.save(commit=False)
        post.position = "article"
        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = ArticleForm
    model = Post
    template_name = 'news_edit.html'


    def form_valid(self, form):
        post = form.save(commit=False)
        post.position = "news"
        return super().form_valid(form)


class ArticleEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'


    def form_valid(self, form):
        post = form.save(commit=False)
        post.position = "article"
        return super().form_valid(form)



class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('posts_list')


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('posts_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('category')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

class Index(NewsEdit):
    def get(self, request):
        string = _('Hello world')

        return HttpResponse(string)



