import requests
from rest_framework import serializers
from gamenews_app.models import Post, User, Category, CategoryPost, CategoryUser, Author

cats = list(map(lambda x: (x.id, x.name), Category.objects.all()))


# Для отображения выпадающего списка в форме
class CategorySerializer(serializers.ModelSerializer):
    name = serializers.MultipleChoiceField(choices=cats)

    class Meta:
        model = Category
        fields = ['name']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CategoryRetriveSerializer(serializers.ModelSerializer):
    subscribers = serializers.SlugRelatedField(slug_field='username', many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'subscribers']


class NewsListSerializer(serializers.ModelSerializer):
    categorys = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    author = serializers.StringRelatedField()  # __str__

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'categorys']


class NewsRetrieveSerializer(serializers.ModelSerializer):
    categorys = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    author = serializers.StringRelatedField()  # __str__

    class Meta:
        model = Post
        exclude = ("watched",)  # все поля кроме просмотров


class NewsCreateSerializer(serializers.ModelSerializer):
    # author = serializers.HiddenField(default=serializers.SerializerMethodField('_user'))
    # author = serializers.SerializerMethodField('_author')

    categorys = CategorySerializer()

    class Meta:
        model = Post
        fields = [
            'text',
            'description',
            'title',
            'small_img',
            'main_img',
            'categorys',
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        user_id = request.user.id
        categorys = validated_data.pop('categorys')  # убираем поле категорий
        validated_data.pop('author', None)  # убираем текущего автора (если есть)
        validated_data.update(
            {'author': Author.objects.get(user_id=user_id)})  # добавляем автора с текущим пользователем
        categorys_set = categorys.get('name', None)  # формируем множество категорий
        p = Post.objects.create(**validated_data)  # создаем обьект Post
        p.categorys.set(categorys_set)  # добавляем в него категории
        return p

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', None)
        instance.description = validated_data.get('description', None)
        instance.title = validated_data.get('title', None)
        instance.small_img = validated_data.get('small_img', None)
        instance.main_img = validated_data.get('main_img', None)
        instance.save()

        categorys_set = validated_data.get('categorys', None).get('name', None)
        instance.categorys.set(categorys_set)
        return instance


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class UserRetriveSerializer(serializers.ModelSerializer):
    categorys = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class UserUpdSerializer(serializers.ModelSerializer):
    # categorys = serializers.SlugRelatedField(slug_field='categorys', many=True, read_only=True)
    categorys = CategorySerializer()

    class Meta:
        model = User
        # fields = "__all__"
        fields = ['categorys']

    def update(self, instance, validated_data):
        categorys_set = validated_data.get('categorys', None).get('name', None)
        instance.categorys.set(categorys_set)
        return instance


class AuthorListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Author
        exclude = ['is_active']


class AuthorListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Author
        exclude = ['is_active', ]


class AuthorRetriveSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Author
        fields = "__all__"


class CategoryUserSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = CategoryUser
        fields = "__all__"


class CategoryUserCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    def create(self, validated_data):
        item = CategoryUser.objects.create(**validated_data)
        return item

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', None)
        instance.user = validated_data.get('user', None)
        instance.save()
        return instance

    class Meta:
        model = CategoryUser
        fields = "__all__"


class CategoryPostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    post = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = CategoryPost
        fields = "__all__"


class CategoryPostCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    post = serializers.SlugRelatedField(slug_field='title', queryset=Post.objects.all())

    def create(self, validated_data):
        item = CategoryPost.objects.create(**validated_data)
        return item

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', None)
        instance.post = validated_data.get('post', None)
        instance.save()
        return instance

    class Meta:
        model = CategoryPost
        fields = "__all__"
