from django.db import models
from users.models import User


class Author(models.Model):
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



class Category(models.Model):
    name = models.CharField(max_length=100)
    subscribers = models.ManyToManyField(User, through='CategoryUser')

    def __str__(self):
        return self.name


class Post(models.Model):
    text = models.TextField(max_length=50 * 1000)
    description = models.CharField(max_length=320)
    title = models.CharField(max_length=80)
    small_img = models.TextField(max_length=500)
    main_img = models.TextField(max_length=500)
    watched = models.IntegerField(default=0)

    date_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categorys = models.ManyToManyField(Category, through='CategoryPost')

    def get_absolute_url(self):
        return f'/{self.id}'


class Comment(models.Model):
    text = models.CharField(max_length=250)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)


class CategoryPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class CategoryUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

