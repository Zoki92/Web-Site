from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView
from .models import Post, Comment
from .forms import CommentForm
from .decorators import user_is_comment_author
from django.contrib import messages
from mptt.forms import TreeNodeChoiceField

# Create your views here.


class BlogFront(TemplateView):
    template_name = 'blog/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.latest('id')
        context['django_post'] = Post.django_posts.order_by('-updated')[0]
        context['lifestyle_post'] = Post.lifestyle_posts.order_by('-updated')[0]
        return context


class DjangoPostsView(ListView):
    queryset = Post.django_posts.order_by('-updated')
    context_object_name = 'django_posts'
    template_name = "blog/django_posts.html"
    paginate_by = 5

class LifestylePostsView(ListView):
    queryset = Post.lifestyle_posts.all().order_by('-updated')
    context_object_name = 'lifestyle_posts'
    template_name = "blog/lifestyle_posts.html"
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        context['form'] = CommentForm
        return context

@login_required
def create_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            if post.category == 'D':
                return redirect('post_detail_django', slug=slug)
            elif post.category == 'L':
                return redirect('post_detail_lifestyle', slug=slug)
        else:
            messages.error(request, f'Please enter text in the comment form')
            if post.category == 'D':
                return redirect('post_detail_django', slug=slug)
            elif post.category == 'L':
                return redirect('post_detail_lifestyle', slug=slug)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
            'form': form
        })

@login_required
def reply_comment(request, slug, comment_id):
    post = get_object_or_404(Post, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form_comment = form.save(commit=False)
            form_comment.post = post
            form_comment.author = request.user
            form_comment.parent = comment
            form_comment.save()
            if post.category == 'D':
                return redirect('post_detail_django', slug=slug)
            elif post.category == 'L':
                return redirect('post_detail_lifestyle', slug=slug)
        else:
            messages.error(request, f'Please enter text in the comment form')
            if post.category == 'D':
                return redirect('post_detail_django', slug=slug)
            elif post.category == 'L':
                return redirect('post_detail_lifestyle', slug=slug)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {
        'form': form
    })

@login_required
@user_is_comment_author
def delete_comment(request, slug, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.post.category == 'D':
        comment.delete()
        return redirect('post_detail_django', slug=slug)
    elif comment.post.category == 'L':
        comment.delete()
        return redirect('post_detail_lifestyle', slug=slug)


@login_required
def redirect_to_blog(request, slug):
    the_post = Post.objects.filter(slug=slug)
    print(the_post.category)
    if request.method == 'GET':
        if the_post.category == 'D':
            return redirect('post_detail_django', slug=slug)
        elif the_post.category == 'L':
            return redirect('post_detail_lifestyle', slug=slug)