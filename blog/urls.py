from django.urls import path
from .views import (BlogFront, DjangoPostsView, LifestylePostsView, PostDetailView,
                    create_comment, reply_comment, delete_comment, redirect_to_blog)


urlpatterns = [
    path('', BlogFront.as_view() , name="blog"),
    path('django/', DjangoPostsView.as_view(), name="django_posts"),
    path('django/<slug:slug>/', PostDetailView.as_view(), name="post_detail_django"),
    path('django/<slug:slug>/comment/', create_comment, name="django_post_comment"),
    path('django/<slug:slug>/comment/<int:comment_id>/reply/', reply_comment, name="django_post_comment_reply"),
    path('django/<slug:slug>/comment/<int:comment_id>/delete/', delete_comment, name="django_post_comment_delete"),
    path('lifestyle/', LifestylePostsView.as_view(), name="lifestyle_posts"),
    path('lifestyle/<slug:slug>/', PostDetailView.as_view(), name="post_detail_lifestyle"),
    path('lifestyle/<slug:slug>/comment/', create_comment, name="lifestyle_post_comment"),
    path('lifestyle/<slug:slug>/comment/<int:comment_id>/reply/', reply_comment, name="lifestyle_post_comment_reply"),
    path('lifestyle/<slug:slug>/comment/<int:comment_id>/delete/', delete_comment, name="lifestyle_post_comment_delete"),
    path('redirect/<slug:slug>', redirect_to_blog, name="redirect_to_blog")


]