from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_view
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from home.models import Post
from .forms import RegisterForm, LoginForm, UserProfileEditForm
from .models import Relations


# Create your views here.

class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        is_following = False
        user = get_object_or_404(User, pk=kwargs['user_id'])
        posts = Post.objects.filter(user=user)
        relations = Relations.objects.filter(from_user=request.user, to_user=user)
        if relations.exists():
            is_following = True
        return render(request, 'users/profile.html', {'user': user, 'posts': posts, 'is_following': is_following})


class UserRegisterView(View):
    form_class = RegisterForm
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])
            user.save()
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
            messages.success(request, 'Wellcome!', extra_tags='success')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = LoginForm
    template_name = 'users/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'wellcome!', extra_tags='success')
                if self.next:
                    return redirect(self.next)
                return redirect('users:user_profile', user.id)
        messages.error(request, 'login or password is invalid', extra_tags='danger')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'logged out', extra_tags='success')
        return redirect('home:home')


class UserPasswordResetView(auth_view.PasswordResetView):
    template_name = 'users/passwordreset/password_reset_form.html'
    success_url = reverse_lazy('users:user_password_reset_done')
    email_template_name = 'users/passwordreset/password_reset_email.html'


class UserPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = 'users/passwordreset/password_reset_done.html'


class UserPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = 'users/passwordreset/password_reset_confirm.html'
    success_url = reverse_lazy('users:user_password_reset_complete')


class UserPasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = 'users/passwordreset/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['user_id'])
        relation = Relations.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, 'You are already following this User', extra_tags='warning')
        else:
            Relations(from_user=request.user, to_user=user).save()
            messages.success(request, 'Followed', extra_tags='success')
        return redirect('users:user_profile', user.id)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['user_id'])
        relation = Relations.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'Unfollowed', extra_tags='success')
        else:
            messages.error(request, 'you are not following this user', extra_tags="warning")
        return redirect('users:user_profile', user.id)


class UserEditView(LoginRequiredMixin, View):
    form_class = UserProfileEditForm
    template_name = 'users/edit_profile.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user.profile, initial={'email': request.user.email})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'Changes Saved', extra_tags='success')
        return redirect('users:user_profile', request.user.id)
