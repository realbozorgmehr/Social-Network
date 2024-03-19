from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import PostCreateForm, PostUpdateForm, CommentCreateForm, CommentReplyCreateForm, SearchForm
from .models import Post, Comment, Vote


# Create your views here.
class HomeView(View):
    form_class = SearchForm

    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        return render(request, 'home/index.html', {'posts': posts, 'form': self.form_class})


# Posts Views
class PostDetailView(View):
    form_class = CommentCreateForm
    form_reply_class = CommentReplyCreateForm
    template_name = 'home/detail.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comment = self.post_instance.pcomments.filter(is_reply=False)
        liked = False
        if request.user.is_authenticated and self.post_instance.user_liked(request.user):
            liked = True
        return render(request, self.template_name,
                      {'post': self.post_instance, 'comments': comment, 'form': self.form_class,
                       'reply_form': self.form_reply_class, 'liked': liked})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'Your comment submitted', extra_tags='success')
            return redirect('home:post_detail', self.post_instance.slug, self.post_instance.id)


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateForm
    template_name = 'home/post_create_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.slug = slugify(form.cleaned_data['title'][:30])
            new_post.save()
            messages.success(request, 'Post Created', extra_tags='success')
            return redirect('home:post_detail', new_post.slug, new_post.id)
        return render(request, self.template_name, {'form': form})


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm
    template_name = 'home/post_update_form.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, 'You cant update another users posts', extra_tags='warning')
            return redirect('home:post_detail', post.slug, post.id)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            updated_post.user = request.user
            updated_post.slug = slugify(form.cleaned_data['title'][:30])
            updated_post.save()
            messages.success(request, 'Post Updated', extra_tags='success')
            return redirect('home:post_detail', updated_post.slug, updated_post.id)
        return render(request, self.template_name, {'form': form})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        if request.user.id == post.user.id:
            post.delete()
            messages.success(request, 'Post Deleted', extra_tags='success')
            return redirect('home:home')
        else:
            messages.error(request, 'You cant delete another users posts', extra_tags='warning')
        return redirect('home:home')


class CommentReplyAddView(LoginRequiredMixin, View):
    form_class = CommentReplyCreateForm

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        comment = get_object_or_404(Comment, pk=kwargs['comment_id'])
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'your comment submitted', extra_tags='success')
        return redirect('home:post_detail', post.slug, post.id)


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, 'You already liked this post', extra_tags='warning')
        else:
            Vote.objects.create(user=request.user, post=post)
            messages.success(request, 'you liked this post', extra_tags='success')
        return redirect('home:post_detail', post.slug, post.id)
