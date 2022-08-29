from django.urls import path
from .views import CommentsView, comment_accept, comment_del

app_name = 'comments'

urlpatterns = [
    path('', CommentsView.as_view(), name='list'),
    path('<int:pk>/del/', comment_del, name='del'),
    path('<int:pk>/accept/', comment_accept, name='accept'),
]
