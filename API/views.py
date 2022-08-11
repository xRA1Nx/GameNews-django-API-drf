from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend

from gamenews_app.models import Post, User, Author, Category, CategoryPost, CategoryUser
from .filters import PostFilterApi
from .paginators import NewsPaginator
from .permissions import IsPostOwnerOrReadOnly, IsCategoryPostOwnerOrReadOnly, IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import NewsListSerializer, NewsRetrieveSerializer, NewsCreateSerializer, \
    CategoryListSerializer, CategoryRetriveSerializer, \
    UserListSerializer, UserRetriveSerializer, UserUpdSerializer, \
    AuthorListSerializer, AuthorRetriveSerializer, \
    CategoryPostSerializer, CategoryPostCreateSerializer, \
    CategoryUserCreateSerializer, CategoryUserSerializer


class CategoryAPIView(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CategoryListSerializer
        else:
            return CategoryRetriveSerializer


class NewsAPIView(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-date_time')
    pagination_class = NewsPaginator
    filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ['categorys', 'date_time']
    filterset_class = PostFilterApi
    # filterset_class = ""

    # permission_classes = [IsOwnerOrReadOnly]
    # permission_classes = [IsAuthorOrReadOnly]

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            permission_classes = [IsPostOwnerOrReadOnly | IsAdminUser]
        else:
            permission_classes = [IsAuthorOrReadOnly | IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "list":
            return NewsListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return NewsCreateSerializer
        else:
            return NewsRetrieveSerializer


class UserAPIView(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return UserListSerializer
        elif self.action == 'retrieve':
            return UserRetriveSerializer
        else:
            return UserUpdSerializer


class AuthorAPIView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    GenericViewSet):
    queryset = Author.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return AuthorListSerializer
        else:
            return AuthorRetriveSerializer


class CategoryUserAPIView(viewsets.ModelViewSet):
    queryset = CategoryUser.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["update", "create", 'partial_update']:
            return CategoryUserCreateSerializer
        else:
            return CategoryUserSerializer


class CategoryPostAPIView(viewsets.ModelViewSet):
    queryset = CategoryPost.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            permission_classes = [IsCategoryPostOwnerOrReadOnly | IsAdminUser]
        else:
            permission_classes = [IsAuthorOrReadOnly | IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ["update", "create", 'partial_update']:
            return CategoryPostCreateSerializer
        else:
            return CategoryPostSerializer
