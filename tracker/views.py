from django.shortcuts import (render, 
                              redirect, 
                              get_object_or_404, 
                              HttpResponseRedirect)
from .models import Workout
from .forms import WorkoutForm

# from django.views.generic.edit import UpdateView

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

def del_workout(request, pk):
    workout = Workout.objects.get(id=pk)

    if request.method == 'POST':
        # delete the band from the database
        workout.delete()
        # redirect to the workout list
        return redirect('workout_list')

    return render(request, 'tracker/delete_workout.html', {'workout': workout})

# class WorkoutUpdateView(UpdateView):
#     model = Workout

#     # specify the fields
#     fields = [
#         "activity",
#         "duration",
#         "date"
#     ]

#     success_url = "/"

def update_workout(request, pk):
    context = {} # dictionary for initial data with 
                # field names as keys
    
    obj = get_object_or_404(Workout, id=pk)

    form = WorkoutForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return redirect(workout_list)

    context['form'] = form
    return render(request, "tracker/workout_form.html", context)