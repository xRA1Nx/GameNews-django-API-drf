from .models import Post, Comment
from django.forms import ModelForm, CharField, Textarea, HiddenInput, TextInput, URLInput, \
    SelectMultiple


class PostAddForm(ModelForm):

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
            'categorys': SelectMultiple(attrs={
                'placeholder': "выберите категорию",
                'class': "inp",
                'size': 7
            })
        }

        labels = {
            'categorys': 'Категории',
        }


class CommentUpdForm(ModelForm):
    text = CharField(
        label='текст',
        widget=Textarea(attrs={'class': 'input-post-comment'})
    )

    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': Textarea(attrs={'class': 'myfieldclass'}),
        }
