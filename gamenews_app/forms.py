from .models import Post, Category
from django.forms import ModelForm, CharField, Textarea, MultipleChoiceField, HiddenInput, TextInput, URLInput, \
    SelectMultiple


class PostAddForm(ModelForm):

    categorys = MultipleChoiceField(
        label="категории",
        choices=Category.get_choices(),
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
