from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task, Comment


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


#------------------------------------------------------------------------------------------------------


class TaskForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'cols': '60'
        }
    ))

    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'deadline',
            'complete'
        )
        help_texts = {
            'deadline': 'Example: 2021-01-31 23:49:00'
        }


#-----------------------------------------------------------------------------------------------------


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment...',
                'rows': '5',
            },
        )
    )

    class Meta:
        model = Comment
        fields = ("body",)


