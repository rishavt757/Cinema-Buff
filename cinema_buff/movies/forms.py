from django import forms
from .models import Rating, Review, Movie, Genre

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['story_score', 'acting_score', 'cinematography_score']
        widgets = {
            'story_score': forms.Select(
                choices=[(i, f'{i}/10') for i in range(1, 11)],
                attrs={'class': 'form-control'}
            ),
            'acting_score': forms.Select(
                choices=[(i, f'{i}/10') for i in range(1, 11)],
                attrs={'class': 'form-control'}
            ),
            'cinematography_score': forms.Select(
                choices=[(i, f'{i}/10') for i in range(1, 11)],
                attrs={'class': 'form-control'}
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['story_score'].label = 'Story/Plot'
        self.fields['acting_score'].label = 'Acting Performance'
        self.fields['cinematography_score'].label = 'Cinematography'

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
        fields = ['title', 'synopsis', 'release_date', 'content_type', 'genres', 'poster']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'synopsis': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Synopsis'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'content_type': forms.Select(attrs={'class': 'form-control'}),
            'genres': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'poster': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
        }
