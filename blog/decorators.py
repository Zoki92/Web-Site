from django.core.exceptions import PermissionDenied
from .models import Comment

def user_is_comment_author(function):
    def wrap(request, *args, **kwargs):
        comment = Comment.objects.get(pk=kwargs['comment_id'])
        if comment.author == request.user or request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
