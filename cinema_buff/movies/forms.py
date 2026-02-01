from django import forms
from .models import Rating, Review, Movie, Genre

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.Select(choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)])
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Review Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your review here...'})
        }

class MovieCreateForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'synopsis', 'release_date', 'genres', 'poster']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie Title'}),
            'synopsis': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Movie Synopsis'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genres': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'poster': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
        }
