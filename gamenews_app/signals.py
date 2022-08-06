from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from gamenews_proj.settings import SITE_URL
from .models import Post
from users.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import Group


@receiver(post_save, sender=User)
def add_user_to_common_group(sender, created, instance, **kwargs):
    if created:
        common_group = Group.objects.get(name='common')
        """
        user соединен с group m2m связью. 
        При такой связи, можно обратиться к связывающей таблице через <related_name>_set
        """
        common_group.user_set.add(instance)


@receiver(m2m_changed, sender=Post.categorys.through)
def send_email_to_subscriber_on_addpost(sender, instance, action='post_add', **kwargs):
    emails_and_users = set()
    for cat in instance.categorys.all():
        emails_and_users.update(cat.get_subscrubers_email_and_name())

    subject = 'Новая статья'
    from_email = 'django.sending@yandex.ru'
    for email, user in emails_and_users:
        to = email
        html_content = render_to_string('email/send_on_post_create.html',
                                        {
                                            "post_add": instance,
                                            "user": user,
                                            "site": SITE_URL}
                                        )
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
