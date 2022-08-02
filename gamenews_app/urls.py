from .views import NewsView, PostView, PostAddView, PostDelView, PostUpdView
from django.urls import path

app_name = 'gnews'

urlpatterns = [
    path('', NewsView.as_view(), name='list'),
    path('<int:pk>', PostView.as_view(), name='detail'),
    path('add/', PostAddView.as_view(), name='add'),
    path('<int:pk>/del/', PostDelView.as_view(), name='del'),
    path('<int:pk>/edit/', PostUpdView.as_view(), name='upd'),

]
