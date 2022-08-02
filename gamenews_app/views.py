from .forms import PostAddForm
from .models import Post, Author

from django.db.models import Count, Case, When
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

qs_comm_count = Post.objects.annotate(count_comments=Count('comment'))


class NewsView(ListView):
    model = Post
    template_name = 'default.html'
    context_object_name = 'news'


    # с помощью annotate Получаем доп поле count_comments содержащее инфо о кол-ве комментариев
    def get_queryset(self):
        return qs_comm_count.order_by('-date_time')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aside'] = qs_comm_count.order_by('-count_comments')[0:3]
        return context


class PostView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_queryset(self):
        return qs_comm_count

    def get_context_data(self, *, object_list=None, **kwargs):
        post_text = self.object.text.split("\n")
        context = super().get_context_data(**kwargs)
        context['post_text'] = post_text
        context['aside'] = qs_comm_count.order_by('-count_comments')[0:3]
        # обращаемся к обьекту post и берем из него все комменты
        context['comments'] = self.object.comment_set.all().order_by('-date_time')
        return context


class PostAddView(CreateView):
    model = Post
    template_name = 'post_add.html'
    form_class = PostAddForm

    # def get_initial(self):
    #     initial = super().get_initial()
    #     user = self.request.user
    #     author = Author.objects.get(user_id=user.pk)
    #     initial['author'] = author
    #     return initial

class PostUpdView(UpdateView):
    model = Post
    template_name = 'post_add.html'
    form_class = PostAddForm



class PostDelView(DeleteView):
    model = Post
    template_name = 'post_del.html'
    success_url = "/"


