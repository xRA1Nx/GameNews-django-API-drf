from django.urls import path, include
from rest_framework import routers
from .views import NewsAPIView, UserAPIView, AuthorAPIView, CategoryAPIView, CategoryPostAPIView, CategoryUserAPIView
from .yasg import urlpatterns as doc_urls

router = routers.DefaultRouter()
router.register(r'news', NewsAPIView)
router.register(r'categorys', CategoryAPIView)
router.register(r'users', UserAPIView)

router.register(r'authors', AuthorAPIView)
router.register(r'CategoryPost', CategoryPostAPIView)
router.register(r'CategoryUser', CategoryUserAPIView)

app_name = 'API'

urlpatterns = [
    path('submit-data/', include(router.urls)),
]

urlpatterns += doc_urls
