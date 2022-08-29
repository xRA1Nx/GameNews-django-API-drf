import re

from allauth.account.models import EmailAddress
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from users.models import User
from gamenews_app.models import Author
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def profile_edit_view(request):
    action = request.GET.get('action')
    user = request.user
    context = {'action': action, 'error': ''}

    # Удаляем аватар
    if action == 'ava-del':
        user.avatar = '/static/imgs/ava-default.svg'
        user.save()
        return redirect('/lk/')

    if request.method == 'POST':
        # Меняем аватар
        if action == 'ava-edit':
            ava = request.POST.get('ava').strip()
            if not ava:
                context['error'] = 'введите ссылку на ваш аватар'
            else:
                user.avatar = ava
                user.save()
                return redirect('/lk/')

        # Меняем фамилию
        if action == "edit-lname":
            reg_ex = r'^[а-я]+$'
            new_lname = request.POST.get('lname').strip()
            if not new_lname:
                context['error'] = 'заполните поле'
            elif len(new_lname) < 2:
                context['error'] = 'Фамилия д.б. длинее 2х букв'
            elif not re.match(reg_ex, new_lname, flags=re.I):
                context['error'] = 'Фамилия должна состоять только из русских букв'
            else:
                User.objects.all().filter(id=user.id).update(lname=new_lname.title())
                return redirect("/lk/")

            # меняем имя
        if action == "edit-fname":
            reg_ex = r'^[а-я]+$'
            new_fname = request.POST.get('fname').strip()
            if not new_fname:
                context['error'] = 'заполните поле'
            elif len(new_fname) < 2:
                context['error'] = 'Имя д.б. длинее 2х букв'
            elif not re.match(reg_ex, new_fname, flags=re.I):
                context['error'] = 'Фамилия должна состоять только из русских букв'
            else:
                User.objects.all().filter(id=user.id).update(fname=new_fname.title())
                return redirect("/lk/")

            # меняем Nick
        if action == "edit-nick":
            new_nick = request.POST.get('nick').strip()
            if not new_nick:
                context['error'] = 'заполните поле'
            elif len(new_nick) < 5:
                context['error'] = 'Ник д.б. длинее 5х символов'
            elif User.objects.all().filter(username__iexact=new_nick.lower()).exists():
                context['error'] = 'Такой ник уже занят'
            else:
                User.objects.all().filter(id=user.id).update(username=new_nick)
                return redirect("/lk/")

            # меняем email
        if action == "edit-email":
            reg_ex = r'^.+@.+$'
            new_email = request.POST.get('email').strip()
            if not new_email:
                context['error'] = 'заполните поле'
            elif len(new_email) < 3:
                context['error'] = 'email д.б. длинее 2х символов'
            elif not re.match(reg_ex, new_email, flags=re.I):
                context['error'] = 'Фамилия должна состоять только из русских букв'
            elif User.objects.all().filter(email__iexact=new_email.lower()).exists():
                context['error'] = 'Такой ник уже занят'
            else:
                User.objects.all().filter(id=user.id).update(email=new_email)
                EmailAddress.objects.all().filter(user_id=user.id).update(email=new_email)
                return redirect("http://127.0.0.1:8000/logout/")

    return render(request, 'profile/profile-edit.html', context)


class DownGrade(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        current_user = request.user
        premium_group = Group.objects.get(name='authors')
        # Если нет в группе авторов такого пользователя, то добавляем в список пользователей этого автора
        if current_user.groups.filter(name='authors').exists():
            premium_group.user_set.remove(current_user)
        # Если не существует такого автора
        if Author.objects.filter(user=current_user).exists():
            Author.objects.update(is_active=False)
        return redirect('/lk/')


@login_required
def upgrade_me(request):
    current_user = request.user
    premium_group = Group.objects.get(name='authors')
    # Если нет в группе авторов такого пользователя, то добавляем в список пользователей этого автора
    if not current_user.groups.filter(name='authors').exists():
        premium_group.user_set.add(current_user)
    # Если не существует такого автора
    if not Author.objects.filter(user=current_user).exists():
        Author.objects.create(user=current_user)
    else:
        Author.objects.update(is_active=True)
        """
        Переадресация на текущую страницу
        """
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('/lk/')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/lk.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        cats = user.categorys.all()
        author = Author.objects.filter(user_id=user.id)
        is_author = author.exists() and author[0].is_active
        context = super().get_context_data(**kwargs)
        fname = user.fname if user.fname else "нет данных"
        lname = user.lname if user.lname else "нет данных"

        context['cats'] = cats
        context['is_author'] = is_author
        context['fname'] = fname
        context['lname'] = lname
        return context
