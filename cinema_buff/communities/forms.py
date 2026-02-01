from django import forms
from .models import DiscussionPost, DiscussionComment

class DiscussionPostForm(forms.ModelForm):
    class Meta:
        model = DiscussionPost
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a descriptive title for your discussion...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Share your thoughts, questions, or recommendations about this genre...'
            })
        }

class DiscussionCommentForm(forms.ModelForm):
    class Meta:
        model = DiscussionComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            })
        }
