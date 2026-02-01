from django import forms
from .models import UserProfile
from movies.models import Genre

class UserProfileForm(forms.ModelForm):
    favorite_genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False
    )
    
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'favorite_genres']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control bg-secondary text-light border-warning',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control bg-secondary text-light border-warning',
                'accept': 'image/*'
            })
        }
