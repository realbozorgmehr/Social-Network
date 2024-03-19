from django import forms

from home.models import Post, Comment


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': "form-control", })
        }


class CommentReplyCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.TextInput(attrs={'class': "form-control", })
        }


class SearchForm(forms.Form):
    search = forms.CharField()
