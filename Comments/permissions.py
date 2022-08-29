from django.db.models import Q

from gamenews_app.models import Author, Comment


def is_active_author(user) -> bool:
    author = Author.objects.filter(user=user)
    return author.exists() and author[0].is_active  # если юзер - автор, и автор активен


def is_authors_comment(user, comment_id) -> bool:
    author = Author.objects.filter(user=user)
    comment = Comment.objects.filter(Q(post__author__user=user) & Q(id=comment_id))
    if not author.exists() or not comment.exists():
        return False
    # если существует коммент с таким id и относящийся к новости  пользователя, являющимся активным автором
    return all([
        author[0].is_active,
        comment.exists(),
        not comment[0].accepted  # при условии что еще не акцептован
    ])
