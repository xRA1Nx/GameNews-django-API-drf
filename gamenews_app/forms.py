from .models import Post, Author, Category
from django.forms import ModelForm, CharField, Textarea, MultipleChoiceField, HiddenInput, TextInput, URLInput, \
    SelectMultiple, ChoiceField, Select

# наполняем choices  для формы
# authors = list(map(lambda x: (x, x.user.username), Author.objects.all()))
cats = list(map(lambda x: (x.id, x.name), Category.objects.all()))


class PostAddForm(ModelForm):
    # author = ChoiceField(
    #     label='авторы',
    #     choices=authors,
    #     widget=Select(attrs={
    #         'placeholder': "выберите автора",
    #         'class': "inp",
    #     })
    # )

    categorys = MultipleChoiceField(
        label="категории",
        choices=cats,
        widget=SelectMultiple(attrs={
            'placeholder': "выберите категорию",
            'class': "inp",
            'size': 7
        }))

    main_img = CharField(
        label="основная картинка",
        widget=URLInput(attrs={
            'placeholder': "ссылка на вашу картинку",
            # 'class': "inp",
        }))

    small_img = CharField(
        label="маленькая картинка",
        widget=URLInput(attrs={
            'placeholder': "ссылка на вашу картинку",
            # 'class': "inp",
        }))
    title = CharField(
        label='заголовок',
        widget=TextInput(attrs={
            'placeholder': "введите заголовок",
            'class': "inp",
        }))
    description = CharField(
        label='Краткое описание:',
        widget=Textarea(attrs={
            'placeholder': "введите заголовок",
            'class': "inp post-preview-ta",
        }))
    text = CharField(
        label='Текст статьи:',
        widget=Textarea(attrs={
            'placeholder': "напишите статью",
            'class': "inp post-ta",
        }))

    class Meta:
        model = Post
        fields = ['categorys', 'main_img', 'small_img', 'title', 'description', 'text', 'author']

        widgets = {
            'author': HiddenInput(),
        }
