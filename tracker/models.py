from django.db import models

class Exercise(models.Model): # this model is a separate, reusable table that can be reused for multiple different workouts
                                # making this into a dropdown menu when adding a workout
    name = models.CharField(max_length=200)
    instructions = models.TextField()
    # images = models.ImageField(upload_to='exercises/', blank=True, null=True)
    muscle_group = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Workout(models.Model):
    title = models.CharField(max_length=200) # creates a text fields that can hold up to 200 characters. 
                                                # this is where you'll store the name of the workout.
    duration = models.IntegerField(help_text="Duration in minutes") # creates a whole number field for storing how many minutes the workout lasted.
                                                                    # The help_text parameter adds a hint that will appear in forms and the admin panel.
    date = models.DateField() # creates a date field for recording when the workout happened.

    exercises = models.ManyToManyField(Exercise, through='WorkoutExercise')

    def __str__(self): # the __str__() method defines how a Workout object appears when printed or displayed in the admin panel.
                        # Instead of seeing something unhelpful like "Workout object (1)," you will see "Running - 30 min on 2025-03-15".
        return f"{self.title} - {self.duration} min on {self.date}"

# The Exercise class is just a model for each individual exercise.
# Connecting Exericse to the Workout model with ManyToManyField says "this exercise is part of this workout".
# The Workoutexercise model will allow the user to put in how many sets/reps they did and the weight they used.
# Any ForeignKey renders as a <select> dropdown by default in a Django ModelForm, listing every row from the related table (using each object's __str__ method as the display text)
'''However, the workout won't be shown as a dropdown because in forms.py, inlineformset_factory's whole purpose is to manage child objects (WorkoutExercise) tied to one specific 
parent (Workout) — the one you pass in as instance=workout in the view. Since the parent is already known, Django auto-fills workout behind the scenes and excludes 
it from the visible form fields. You only see exercise, sets, reps, weight as dropdowns/inputs.'''
class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE) # on_delete=models.CASCADE tells Django to delete all related exericse when the workout is deleted
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE) 
    sets = models.PositiveIntegerField(default=3)
    reps = models.PositiveIntegerField(default=8)
    weight = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True)

    def __str__(self):
        return f"{self.exercise.name} - {self.sets}x{self.reps}"
