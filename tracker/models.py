from django.db import models

class Exercise(models.Model): # this model is a separate, reusable table that can be reused for multiple different workouts
                                # making this into a dropdown menu when adding a workout
    name = models.CharField(max_length=200)
    instructions = models.TextField()
    images = False
    muscle_group = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Workout(models.Model):
    activity = models.CharField(max_length=200) # creates a text fields that can hold up to 200 characters. 
                                                # this is where you'll store the name of the excersize like "Running" or "Cycling".
    duration = models.IntegerField(help_text="Duration in minutes") # creates a whole number field for storing how many minutes the workout lasted.
                                                                    # The help_text parameter adds a hint that will appear in forms and the admin panel.
    date = models.DateField() # creates a date field for recording when the workout happened.

    exercises = models.ManyToManyField(Exercise)

    def __str__(self): # the __str__() method defines how a Workout object appears when printed or displayed in the admin panel.
                        # Instead of seeing something unhelpful like "Workout object (1)," you will see "Running - 30 min on 2025-03-15".
        return f"{self.activity} - {self.duration} min on {self.date}"

# The Exercise class is just a model for each individual exercise.
# Connecting Exericse to the Workout model with ManyToManyField says "this exercise is part of this workout".
# The Workoutexercise model will allow the user to put in how many sets/reps they did and the weight they used.
class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE) # on_delete=models.CASCADE tells Django to delete all related exericse when the workout is deleted
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField(default=3)
    reps = models.PositiveIntegerField(default=8)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
