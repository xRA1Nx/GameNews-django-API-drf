from django.db import models
from django.db.models import CharField
from users.models import User


class Author(models.Model):
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    subscribers = models.ManyToManyField(User, through='CategoryUser', related_name='categorys')

    def __str__(self) -> CharField:
        return self.name

    # добавляем метод возрващающий список email подписчиков категории
    def get_subscrubers_email_and_name(self) -> set:
        res = set()
        for user in self.subscribers.all():
            res.add((user.email, user))
        return res

    @staticmethod
    def get_choices() -> list:
        return list(map(lambda x: (x.id, x.name), Category.objects.all()))


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

    def __str__(self) -> CharField:
        return self.title

    def get_absolute_url(self) -> str:
        return f'/{self.id}'


class Comment(models.Model):
    text = models.CharField(max_length=250)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def get_absolute_url(self) -> str:
        return f'/{self.post.id}#comment-{self.id}'


class CategoryPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='news')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cats')


class CategoryUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
