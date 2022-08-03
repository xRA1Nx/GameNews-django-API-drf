from users.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
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


