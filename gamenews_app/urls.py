from .views import NewsView, PostView, PostAddView, PostDelView, PostUpdView, \
    subscrib, unscrib, comment_add_view, comment_del_view, CommentUpdView
from django.contrib.auth.views import LogoutView
from django.urls import path

app_name = 'gnews'

urlpatterns = [
    path('', NewsView.as_view(), name='list'),
    path('<int:pk>/', PostView.as_view(), name='detail'),
    path('add/', PostAddView.as_view(), name='add'),
    path('<int:pk>/del/', PostDelView.as_view(), name='del'),
    path('<int:pk>/edit/', PostUpdView.as_view(), name='upd'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('subscribe/<int:pk>/', subscrib, name='subscribe'),
    path('unscribe/', unscrib, name='unscribe'),
    path('<int:pk>/comment-add/', comment_add_view, name='comment-add'),
    path('comment-del/<int:pk>', comment_del_view, name='comment-del'),
    path('<int:post_pk>/comment-upd/<int:pk>/', CommentUpdView.as_view(), name='comment-upd'),

]
