from celery import shared_task
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from NewsPortal.news.models import Post, Category
@shared_task
@receiver(post_save, sender=Post)
def product_created(id,  **kwargs):
    post = Post.objects.get(pk = id)
    emails = User.objects.filter(
        subscriptions__category=post.category.all()
    ).values_list('email', flat=True)

    subject = f'Новый товар в категории {post.category}'

    text_content = (
        f'Товар: {post.heading}\n'
        f'Цена: {post.author}\n\n'
        f'Ссылка на товар: http://127.0.0.1:8000{post.get_absolute_url()}'
    )
    html_content = (
        f'Товар: {post.heading}<br>'
        f'Цена: {post.author}<br><br>'
        f'<a href="http://127.0.0.1{post.get_absolute_url()}">'
        f'Ссылка на товар</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def week_email():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=last_week)
    categories = set(posts.values_list('category__category', flat=True))
    subscribers = set(Category.objects.filter(category__in=categories).values.list('subscribers__email', Flat=True))
    html_content = render_to_string('daily_post.html', {'link': settings.SITE_URL, 'posts': posts})
    msg = EmailMultiAlternatives(subject='Статьи за неделю', body='', from_email=settings.DEFAULT_FROM_EMAIL,
                                 to=subscribers, )

    msg.attach_alternative(html_content, 'text/html')

