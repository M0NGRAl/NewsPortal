from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Author(models.Model):
     author = models.OneToOneField(User, on_delete=models.CASCADE)
     rating = models.IntegerField(default=0)

     def update_rating(self):
         post_ratings = self.post_set.aggregate(total=models.Sum('rating'))
         post_rating_total = post_ratings * 3

         # Суммарный рейтинг всех комментариев автора
         author_comments_ratings = self.user.comment_set.aggregate(total=models.Sum('rating'))

         # Суммарный рейтинг всех комментариев к статьям автора
         post_comments_ratings = Comment.objects.filter(post__author=self).aggregate(total=models.Sum('rating'))

         # Общий рейтинг автора
         self.rating = post_rating_total + author_comments_ratings + post_comments_ratings
         self.save()

     def __str__(self):
         return self.author.username  # Возвращаем имя пользователя





class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category


class Post(models.Model):
    news = "NE"
    article = "AR"
    POSITION = [(news, "Новость"),(article, "Статья")]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    position =models.CharField(max_length=2, choices=POSITION)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    heading = models.TextField()
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + "..."

    def __str__(self):
        formatted_time = self.time_in.strftime('%d %B %Y')
        return f'{self.heading}: {formatted_time}: {self.text}'

    def get_absolute_url(self):
        return reverse('posts_detail', args=[str(self.id)])



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


