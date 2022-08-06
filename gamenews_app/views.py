from django.http import HttpResponseRedirect

from .forms import PostAddForm
from .models import Post, Author, Category
from django.db.models import Count, Case, When, Q
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

# с помощью annotate Получаем доп поле count_comments содержащее инфо о кол-ве комментариев
qs_comm_count = Post.objects.annotate(count_comments=Count('comment'))


@login_required
def subscrib(request, **kwargs):
    post = Post.objects.get(id=kwargs['pk'])
    user = request.user
    for cat in post.categorys.all():
        if user not in cat.subscribers.all():
            cat.subscribers.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def unscrib(request, **kwargs):
    user = request.user
    cat_id = request.POST.get('cat_id')
    cat = Category.objects.get(id=cat_id)
    if user in cat.subscribers.all():
        cat.subscribers.remove(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class NewsView(ListView):
    model = Post
    template_name = 'default.html'
    context_object_name = 'news'
    paginate_by = 9

    def get_queryset(self):
        category = self.request.GET.get('category')
        query = qs_comm_count.order_by('-date_time')
        text = self.request.GET.get('text')

        # Если производится поиск , т.е. существует get параметр text
        if text:
            text = text.strip()
            query = query.filter(Q(title__icontains=text) | Q(text__icontains=text) | Q(description__icontains=text))

        # Если новость фильтруют по категории , т.е. существует get параметр category
        if category:
            query = query.filter(categorys__name__icontains=category)

        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        category = self.request.GET.get('category')
        text = self.request.GET.get('text')

        url_category = f"&category={category}" if category else ""
        url_search = f"&text={text.strip()}" if text else ""

        context = super().get_context_data(**kwargs)
        context['aside'] = qs_comm_count.order_by('-count_comments')[0:3]
        # context['url_category'] = url_category # дополняем get параметр в пагинации
        # context['url_search'] = url_category+url_search  # дополняем get параметр в пагинации
        context['GET_params'] = url_category + url_search  # дополняем get параметр в пагинации

        return context


class PostView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_queryset(self):
        return qs_comm_count

    def get_context_data(self, *, object_list=None, **kwargs):
        cur_user = self.request.user
        is_author = cur_user.is_authenticated and Author.objects.filter(user=cur_user).exists()

        is_subscriber = False
        cats = self.object.categorys.all()
        for cat in cats:
            if cur_user in cat.subscribers.all():
                is_subscriber = True
                break

        post_text = self.object.text.split("\n")
        context = super().get_context_data(**kwargs)
        context['post_text'] = post_text
        context['is_author'] = is_author
        context['aside'] = qs_comm_count.order_by('-count_comments')[0:3]
        context['is_subscriber'] = is_subscriber
        # обращаемся к обьекту post и берем из него все комменты
        context['comments'] = self.object.comment_set.all().order_by('-date_time')
        return context


class PostAddView(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'post_add.html'
    form_class = PostAddForm
    permission_required = 'gamenews_app.add_post'

    # def get_initial(self):
    #     initial = super().get_initial()
    #     user = self.request.user
    #     author = Author.objects.get(user_id=user.pk)
    #     initial['author'] = author
    #     return initial


class PostUpdView(PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_add.html'
    form_class = PostAddForm
    permission_required = 'gamenews_app.change_post'


class PostDelView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_del.html'
    success_url = "/"
    permission_required = 'gamenews_app.delete_post'
