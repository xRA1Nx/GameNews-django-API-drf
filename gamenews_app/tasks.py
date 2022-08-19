from celery import shared_task
import datetime

from gamenews_proj.settings import SITE_URL
from .models import Post, Category
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from time import sleep
import time


# @shared_task
# def printer(n):
#     for i in range(n):
#         sleep(1)
#         print(i + 1)


@shared_task
def celery_every_week_notify():
    delta = datetime.timedelta(7)
    start_date = datetime.datetime.utcnow() - delta
    end_date = datetime.datetime.utcnow()
    posts_for_week_send = Post.objects.filter(date_time__range=(start_date, end_date))
    emails_and_users = set()

    # формируем уникальное множество из кортеджей (емейл, имя) пользователей
    for cat in Category.objects.all():
        emails_and_users.update(cat.get_subscrubers_email_and_name())

    subject = 'Ваша подписка на GameNews. Еженедельная рассылка от CELERY'
    from_email = 'django.sending@yandex.ru'

    for email, user in emails_and_users:
        categorys = user.categorys.all().filter(post__in=posts_for_week_send)
        to = email
        html_content = render_to_string('email/evere_week_send.html',
                                        {
                                            "posts": posts_for_week_send,
                                            "cats": categorys,
                                            "user": user,
                                            "site": SITE_URL}
                                        )
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    print("письма отправлены")
