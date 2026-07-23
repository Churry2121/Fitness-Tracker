from django.db import models

# Create your models here.
class Workout(models.Model):
    activity = models.CharField(max_length=200) # creates a text fields that can hold up to 200 characters. 
                                                # this is where you'll store the name of the excersize like "Running" or "Cycling".
    duration = models.IntegerField(help_text="Duration in minutes") # creates a whole number field for storing how many minutes the workout lasted.
                                                                    # The help_text parameter adds a hint that will appear in forms and the admin panel.
    date = models.DateField() # creates a date field for recording when the workout happened.

    def __str__(self): # the __str__() method defines how a Workout object appears when printed or displayed in the admin panel.
                        # Instead of seeing something unhelpful like "Workout object (1)," you will see "Running - 30 min on 2025-03-15".
        return f"{self.activity} - {self.duration} min on {self.date}"