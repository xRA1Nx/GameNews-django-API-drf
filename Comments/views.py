from django.db.models import Q
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

from .permissions import is_active_author, is_authors_comment
from gamenews_app.models import Comment
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required


class CommentsView(PermissionRequiredMixin, ListView):
    model = Comment
    template_name = 'profile/user-comments.html'
    context_object_name = 'comments'
    paginate_by = 10
    permission_required = 'gamenews_app.view_comment'

    def get_queryset(self):
        return Comment.objects.filter(Q(post__author__user=self.request.user) & Q(accepted=False))

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return res if is_active_author(request.user) else HttpResponseForbidden()


@permission_required('gamenews_app.delete_comment', raise_exception=True)
def comment_del(request, **kwargs):
    comment_id = kwargs.get('pk')
    if not is_authors_comment(request.user, comment_id):
        return HttpResponseForbidden()
    Comment.objects.get(id=comment_id).delete()
    return redirect("/comments")


@permission_required('gamenews_app.change_comment', raise_exception=True)
def comment_accept(request, **kwargs):
    comment_id = kwargs.get('pk')
    if not is_authors_comment(request.user, comment_id):
        return HttpResponseForbidden()
    Comment.objects.filter(id=comment_id).update(accepted=True)
    return redirect("/comments")
