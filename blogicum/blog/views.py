from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm, PostForm, UserUpdateForm
from .models import Category, Comment, Post

User = get_user_model()


class CommentMixin:
    """
    Adds model, form_class, template_name attributes and modified method
    get_success_url.
    """

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def get_success_url(self):
        """
        Determines the URL to redirect the user to the correct post when the
        CommentForm is successfully filled in & processed.
        """
        return reverse(
            'blog:post_detail', kwargs={'post_pk': self.kwargs['post_pk']}
        )


class CommentDispatchMixin:
    """Adds pk_url_kwarg attribute and modified method dispatch."""

    pk_url_kwarg = 'comment_pk'

    def dispatch(self, request, *args, **kwargs):
        """
        Gets the correct comment, or raises 404 error
        if the comment does not exist.
        Redirects to the post page if comment author is not equal to the
        request user.
        """
        comment = get_object_or_404(Comment, pk=kwargs[self.pk_url_kwarg])
        if comment.author != request.user:
            return redirect(
                'blog:post_detail', post_pk=kwargs['post_pk']
            )
        return super().dispatch(request, *args, **kwargs)


class PostDispatchMixin:
    """
    Adds model, form_class, template_name, pk_url_kwarg attributes and
    modified method dispatch.
    """

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_pk'

    def dispatch(self, request, *args, **kwargs):
        """
        Gets the correct post, or raise 404 error if the post does not exist.
        Redirects to the post page if post author is not equal to the
        request user.
        """
        post = get_object_or_404(Post, pk=kwargs[self.pk_url_kwarg])
        if post.author != self.request.user:
            return redirect(
                'blog:post_detail',
                post_pk=kwargs[self.pk_url_kwarg]
            )
        return super().dispatch(request, *args, **kwargs)


class PaginateMixin:
    """Adds model and paginate_by attributes"""

    model = Post
    paginate_by = settings.POSTS_ON_PAGE


class HomepageListView(PaginateMixin, ListView):
    """
    Displays homepage with all posts, based on the "index.html"
    template.
    """

    template_name = 'blog/index.html'
    queryset = Post.published.all()


class CategoryListView(PaginateMixin, ListView):
    """
    Displays posts under specific category, using the "category.html"
    template.
    """

    slug_url_kwarg = 'category_slug'
    template_name = 'blog/category.html'

    def get_queryset(self):
        """
        Returns the QuerySet of the specific category.
        If this category does not exist or this category is not published,
        raises 404 error.
        """
        category = get_object_or_404(
            Category, slug=self.kwargs[self.slug_url_kwarg], is_published=True
        )
        queryset = category.posts.published()
        return queryset

    def get_context_data(self, **kwargs):
        """Adds information about the category to the context."""
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category, slug=self.kwargs['category_slug']
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Displays UserUpdateForm with user instance, based on the "user.html"
    template.
    """

    model = User
    form_class = UserUpdateForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        """Returns the username from the request."""
        return self.request.user

    def get_success_url(self):
        """
        Sets the URL for redirect to the correct user profile when the
        UserUpdateForm is successfully filled in & processed.
        """
        return reverse('blog:profile', kwargs={'username': self.request.user})


class ProfileListView(PaginateMixin, ListView):
    """
    Displays posts of the specific author, based on the "profile.html"
    template.
    """

    template_name = 'blog/profile.html'

    def get_queryset(self):
        """
        Returns the published QuerySet of the specific author
        if request user is not equal to the author.
        Returns all posts of the author if request user is equal to the author.
        Raises 404 error if there is no correct author.
        """
        author = get_object_or_404(User, username=self.kwargs['username'])
        if self.request.user == author:
            queryset = author.posts.with_related_data()
        else:
            queryset = author.posts.with_related_data().filter(
                author=author
            )
        return queryset

    def get_context_data(self, **kwargs):
        """Adds information about the user to the context."""
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Displays PostForm based on "create.html" template."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        """Adds the author to the form."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Sets the URL for redirect to the correct user profile when the
        UserCreateForm is successfully filled in & processed.
        """
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user}
        )


class PostDetailView(DetailView):
    """Displays correct post based on "detail.html" template."""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_pk'

    def dispatch(self, request, *args, **kwargs):
        """
        Gets the correct post, or raises 404 error if the post does not exist.
        Raises 404 error if post author is not equal to the request user and
        post is not published.
        """
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        if post.is_published is False and request.user != post.author:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Adds the CommentForm and post comments to the context."""
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class PostUpdateView(PostDispatchMixin, LoginRequiredMixin, UpdateView):
    """
    Displays PostForm with post instance based on the "create.html"
    template.
    """

    def get_success_url(self):
        """
        Determines the URL for redirect to the correct post when the
        PostForm is successfully filled in & processed.
        """
        return reverse(
            'blog:post_detail', kwargs={'post_pk': self.kwargs['post_pk']}
        )


class PostDeleteView(PostDispatchMixin, LoginRequiredMixin, DeleteView):
    """CBV that displays post information based on "create.html" template."""

    def get_context_data(self, **kwargs):
        """Adds the PostForm with related instance to the context."""
        context = super().get_context_data(**kwargs)
        instance = Post.objects.get(pk=self.kwargs['post_pk'])
        context['form'] = PostForm(instance=instance)
        return context

    def get_success_url(self):
        """
        Determines the URL for redirect to the correct user profile when the
        PostForm is successfully filled in & processed.
        """
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user}
        )


class CommentCreateView(CommentMixin, LoginRequiredMixin, CreateView):
    """Displays CommentForm based on "comment.html" template."""

    def form_valid(self, form):
        """Adds the author and post to the form."""
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)


class CommentDeleteView(
    CommentMixin, CommentDispatchMixin, LoginRequiredMixin, DeleteView
):
    """Displays comment information based on "comment.html" template."""

    pass


class CommentUpdateView(
    CommentMixin, CommentDispatchMixin, LoginRequiredMixin, UpdateView
):
    """
    Displays CommentForm with comment instance based on "comment.html"
    template.
    """

    pass
