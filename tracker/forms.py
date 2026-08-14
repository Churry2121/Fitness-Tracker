from django import forms
import django_filters
from .models import Workout, WorkoutExercise
from django.forms import inlineformset_factory, Select

class WorkoutForm(forms.ModelForm): # ModelForm automatically gnerates form fields based on a model.
    class Meta: # class Meta: model = Workout - this is the explicit link. Django introspects author's fields becuase you told it to.
        model = Workout
        # fields = ['activity', 'duration', 'date']
        fields=['title', 'date', 'duration']
        widgets = { # The widgets dictionary tells Django to render the date field as an HTML date picker instead of a plain text input.
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

WorkoutExerciseFormSet = inlineformset_factory(# to be able to log a workout w/ mutliple exercises in it at one page
    Workout, 
    WorkoutExercise,
    fields=['exercise', 'sets', 'reps', 'weight'],
    extra=3,          # how many empty exercise rows to show
    widgets={
        'exercise': Select(attrs={'class': 'exercise-select'}),
    },
    can_delete=False
)

WorkoutExerciseUpdateFormSet = inlineformset_factory( 
    Workout, WorkoutExercise,
    fields=['exercise', 'sets', 'reps', 'weight'],
    extra=1,
    widgets={
        'exercise': Select(attrs={'class': 'exercise-select'}),
    },
    can_delete=True # only shows when the user updates their workout
)

# class ExerciseFilter(django_filters.FilterSet):
#     query = django_filters.CharFilter(
#         field_name='name',
#         lookup_expr='icontains',
#         label='Search Exercise'
#     )

#     class Meta:
#         model = Exercise
#         fields = []

        