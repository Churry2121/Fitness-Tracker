from django import forms
from .models import Workout

class WorkoutForm(forms.ModelForm): # ModelForm automatically gnerates form fields based on a model.
    class Meta: # class Meta: model = Workout - this is the explicit link. Django introspects author's fields becuase you told it to.
        model = Workout
        fields = ['activity', 'duration', 'date']
        widgets = { # The widgets dictionary tells Django to render the date field as an HTML date picker instead of a plain text input.
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

        