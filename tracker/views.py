from django.shortcuts import render, redirect
from .models import Workout
from .forms import WorkoutForm

# Create your views here.
def workout_list(request): # this view handles the page that displays all workouts
                            # It queries the database for every Workout object, orders 
                            # them by date (most recent first, thanks to the - prefix), 
                            # and passes that list to a template called workout_list.html.
    workouts = Workout.objects.all().order_by('-date')
    return render(request, 'tracker/workout_list.html', {'workouts': workouts}) # render() combines the template with the 
                                                                                # data nad returns the finished HTML page

def add_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workout_list')
    else:
        form = WorkoutForm()
    return render(request, 'tracker/add_workout.html', {'form': form})
