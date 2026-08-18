When creating the django project, make sure to type:
> django-admin startproject project_name .
emphasizing the dot at the end of the command because it tells Django to create the project files in your current directory isntead of creating an extra nested folder.

Also, if you have problem setting the project to a existing repo in github (usually because of SSH keys), you can ignore that by switching to HTTPS instead, which just prompts for a Github username + personal access token:
> git remote set-url origin https://gihub.com/username/repo_name
> git push -u origin main

To create a Django app within the main project folder:
> python manage.py startapp app_name

## How to Register the App
Django doesn't automatically know about your new app. You need to tell it by adding the app to the INSTALLED_APPS list in settings.py file.

Django has already installed a couple apps where many common features are ready to use out of the box.
- 'django.contrib.admin' : Powers the built-in admin dashboard, letting you manage your data through a web interface.
- 'django.contrib.auth' : Handles users, login systems, permissions, and password management.
- 'django.contrib.contenttypes' : Helps Django track and manage relationships between different models.
- 'django.contrib.sessions' : Stores user session data, so users stay logged in across requests.
- 'django.contrib.messages' : Lets you show temporary notifications like success or error messages.
- django.contrib.staticfiles' : Manages static assets such as CSS, JavaScript, and images

## Creating a workout model
A model in Django is a Python class that defines the structure of your data. Each model maps directly to a table in your database. Each attribute on the model becomes a column in that table. 

Think of a model as a blueprint for spreadsheet. The class name is the name of the spreadsheet, and each field is a column header. Every time you save a new workout, Django creates a new row in that spreadsheet.

# Applying Migraions
After defining your model, you need to run migrations so Django can create a database for that model. Migrations are Django's way of translating your Python model definitions into database instructions. Migrations are done in two steps. 

When you change a model (e.g., adding a field, removing a field, etc) you create a new migration that describes that change. You can do this using the makemigrations command. Then you apply the migration using the migrate command and Django updates the database to match.

Run:
> python manage.py makemigrations

You should see output like this:
`Migrations for 'tracker': tracker/migrations/0001_initial.py 
    + Create model Workout`

What this means is Django inspected your Workout model and created a migration file that describes how to build the corresponding database table. You can find this file at tracker/migrations/0001_initial.py.

Then, apply the migration:
> python manage.py migrate

When the migrate command runs, we can see the exact SQL commands that Django used to build and change the database.
Run this command (**not really necessary**):
> python manage.py sqlmigrate tracker 0001

## How to Register the Model in the Admin Panel
Django comes with an admin interface built in. It gives you graphical way to view, add, edit, and delete records in your database w/o writing any extra code. This allows you to quickly test your models and see your data.

But by default, it doesn't know:
- Which models you want to manage
- How you want them displayed

So you register models in admin.py to tell Django to include the specific model in the admin interface.

To add a model to admin, open tracker/admin.py and add the following code:
```python
from djanog.contrib import admin
from .models import Workout
```

To access the admin panel, you need an admin account. Create one by running:
>python manage.py createsuperuser
Django will prompt you for a username, email address, and password. The email is optionl; you can press Enter to skip it.

To access the admin panel, start the development server and navigate to https://127.0.0.1:8000/admin/ in your browser.

To test your model, add one or two test workouts. 

## How to Create Views for the App
A view in Django is a Python function (or class) that receives a web request and returns a web response. That response could be an HTML page, a redirect, a 404 error, or anything else a browser can handle.

Views decide what data to fetch, what processing to do, and what to show the user.

For the fitness tracker, you need two views: one to display the form where users add a workout, an done to display the list of all saved workouts.

### How to create a Form Class
Before writing the views, you need a Django form that handles the workout input.

Django forms are a built-in way to handle user input like login forms, contact forms, or anything that collects data from a user. Instead of manually writing HTML, validating inputs, and handling errors, Django gives you a structured way to do all of that in one place.

Most user inputs are based on the models you’ve created, and Django can automatically generate forms from those models using ModelForms, which speeds things up significantly.

Let's create a new file called forms.py in the tracker folder and add the following code:
```python
from django import forms
from .models import Workout

class WorkoutForm(forms.ModelForm): # ModelForm automatically gnerates form fields based on a model.
    class Meta: # class Meta: model = Workout - this is the explicit link. Django introspects author's fields becuase you told it to.
        model = Workout
        fields = ['activity', 'duration', 'date']
        widgets = { # The widgets dictionary tells Django to render the date field as an HTML date picker instead of a plain text input.
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
```
We can actually see the forms being automatically created by Django. For this we need to enter the shell. In the terminal, type the following command:
> python manage.py shell

Then import the WorkoutForm class that was just created. Type the following code:
> from tracker.forms import WorkoutForm
Then create an object of the WorkoutForm class and print it.:
```shell
workoutform = WorkoutForm()
print(workoutform)
```
You should get a output that looks like an HTML layout, containing the id's of the fields of the form you created (i.e. id_activity, id_duration, id_date).

### Writing Views
In the tracker/views.py file, type the following code:
```python
from django.shortcuts import render, redirect
from .models import Workout

def workout_list(request):
    workouts = Workout.objects.all().order_by('-date')
    return render(request, 'tracker/workout_list.html', {'workouts': workouts})
```
To create the logic to add a workout, first add the Workout form import at the end of the import seciton. Then add the following code after the workout_list view:
```python
from django.shortcuts import render, redirect
from .models import Workout
from .forms import WorkoutForm

# view to list all the workouts
def workout_list(request):
    workouts = Workout.objects.all().order_by('-date')
    return render(request, 'tracker/workout_list.html', {'workouts': workouts})

# view to add a workout
def add_workout(request):
    if request.method == 'POST': # request method: POST when user fills and submits form
        form = WorkoutForm(request.POST)
        if form.is_valid(): # if the form is valid, the form is saved
            form.save()
            return redirect('workout_list')
    else: # else: request method=GET renders a blacnk form and renders it
        form = WorkoutForm()
    return render(request, 'tracker/add_workout.html', {'form': form})
```

## How to Create Templates
Django looks for templates inside a templates folder within each app. Create the following folder structure inside your tracker app: tracker/templates/tracker.
The double tracker folder name is a Django convention called template namespacing. It prevents nameing conflicts if you have multiple apps with templates that share the same filename.

## How to Connect URLs
You need to map URLs to views so that visiting specific address in the browser triggers the right view function.

**How to create App Level URLs:**
Create a new file called tracker/urls.py and add the following code:
```python
from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.workout_list, name='workout_list'), 
    path('add/', views.add_workout, name='add_workout'), 
]
```
Each path function takes 3 arguments: 
1) The route string that represents a URL pattern (an empty string means the root of the app)
2) The view function to call when that URL is visited.
3) A name you can use to reference this URL elsewhere in your code, like the {% url %} template tags.

Now that your app-level URLs are set up, the next step is to connect them to the main project so Django knows where to start routing requests. Open fitness_project.urls.py and update it to include your app's URLs:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),
]
```
The include() function tells Django to look at the URL patterns defined in the tracker/urls.py file whenever someone visits your site. **The empty string prefix means your tracker app handles requests at the root of the site**.

When someone visits http://127.0.0.1:8000/add/, Django first checks fitness_project/urls.py. It matches the empty prefix and delegates to tracker/urls.py. There, it matches add/ and calls the add_workout view.

## How to Prepare for Deployment
Running your app on localhost is great for development, but nobody else can see it. Deployment means putting your app on a server that's accessible from anywhere on the internet. Before you deploy, you'll need to make a few changes to your project's settings.

Open fitness_project/settings.py and make the following changes.
First, set DEBUG to False. In production, these error pages would expose sensitive information about your code and server to anyone who triggers an error.

Next, update ALLOWED_HOSTS to include **PythonAnywhere**'s domain. This setting tells Django which domain names are allowed to serve your app. Replace your username with the acutal PythonAnywhere username you will create next.
`ALLOWED_HOST = ['yourusername.pythonanywhere.com].

Finally, add a STATIC_ROOT setting so Django knows where to collect your static files (CSS, JavaScript, images) for production:
```python
import os
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

**Note:** For a production app handling real user data, you would also want to set a secure SECRET_KEY, configure a proper database like PostgreSQL, and set up HTTPS. But for a learning project, these changes are enough.

## Trials & Error
When trying to link a delete icon to a template (delete_workout.html), I did this:
```html
<div>
    <a href="{% url 'delete_workout' %}"><i class="material-symbols-outlined">delete</i></a>
</div>
```
Django returned a NoReverseMatch error; Reverse for 'delete_workout' with no arguments not found. 1 pattern(s) tried: ['delete/(?P<pk>[0-9]+)\\Z']

In the tracker/urls.py file, my url path for the delete_workout template was this: `path('delete/<int:pk>',...)`, meaning it is expecting a pk argument `(delete/(?P<pk>[0-9]+))`, but in workout_list.html I am calling it with no argument:
```html
<a href="{% url 'delete_workout' %}">
```

I need to pass the specific workout's primary key so Django knows which workout to delete:
```html
<a href="{% url 'delete_workout' workout.pk %}">
```

### Django Generic View: UpdateView
An UpdateView is a built-in class-based view used to edit an existing record in the database. It automatically handles fetching the record, showing a pre-filled form, validating input, and saving changes.
- Specify the model that contains the record to be updated.
- Define the form fields that should appear in the update form.
- Provide the template used to render the form.
- Set a success URL to redirect after the update is saved.

To create an UpdateView, it is only necessary to specify the model. Django’s UpdateView will then look for a template named app_name/modelname_form.html. Then, create a class-based view in tracker/views.py. Then, map it to tracker/urls.py

### Function-Based views.update_workout
`form = WorkoutForm(request.POST or None, instance=obj)`
- instace=obj : since WorkoutForm is a ModelForm (defined in forms.py), Django looks at each field in the form, finds the matching attribute in obj (e.g. obj.activity, obj.duration, obj.date), and use those values as **initial data for each field's widget**.

### Using ForeignKey
Workout (id=5, "Push Day")          Exercise (id=12, "Bench Press")
        \                                   /
         \                                 /
          WorkoutExercise (id=1)
          - workout_id = 5   <- FK to Workout
          - exercise_id = 12 <- FK to Exercise
          - sets = 4, reps = 8, weight = 135

### Loading the exercise.json file
Create a folder in your app: management/commands/exercise.json

```python
import json
from pathlib import Path # modern way to handle file paths
from django.core.management.base import BaseCommand # Every custom Django management command (the things you run with python manage.py <something>) must inherit from BaseCommand.
from tracker.models import Exercise

class Command(BaseCommand):
    help = "Load exercises from a JSON file into the Exercise model" # This is the description shown when you run python manage.py help load_exercises.

    def add_arguments(self, parser):
        parser.add_argument(
            '--file', # defines optional --file flag
            type=str,
            default='tracker/fixtures/exercises.json', # if --file isn't passed, this is the default file path
            help='Path to the JSON file'
        )

        # so, this lets you run the command: python manage.py load_exercises

    def handle(self, *args, **options):
        file_path = Path(options['file'])

        if not file_path.exists():
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        with open(file_path, 'r', encoding='utf-8') as f: # reading the file as utf-8
            data = json.load(f)

        created_count = 0
        skipped_count = 0 # an exercise will be skipped when its name appears more than one in the database

        for entry in data: # loops over each dict in the list
            # Each entry looks like:
            # {"name":"Barbell Squat", "instructions": "...", "muscle_group": "Legs"}}
            exercise, created = Exercise.objects.get_or_create(
                name=entry['name'],
                defaults={
                    'instructions': entry.get('instructions', ''),
                    'muscle_group': entry.get('muscle_group', ''),
                }
            )

            # counter is used for feedback
            if created:
                created_count += 1
            else:
                skipped_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created {created_count} exercises, skipped {skipped_count} duplicates."
        ))  
```
The get_or_create does two things:
- It looks in the database for an Exercise where name matches entry['name'].
- If found, it returns that existing object and created=False.
- If not found, it creates a new Exercise using name plus everything in defaults, and returns created=True.

The name is the lookup key. The instructions and muscle_group of each entry is an empty string '' so if it is empty for that specific exercise, the app won't crash.

Use self.stdout.write() instead of just print() because it respect Django's testing/output-capturing infrastructure (so tests can check command output cleanly)

get_or_create first tries to find an Exercise row where name matches entry['name']. Only if it doesn't find one does it create a new row using name + whatever's in defaults. And if you run the `python manage.py load_exercises` command twice, the object was already created in the first run. Any new entries will then be created if added any. We use get_or_create instead of Exercises.objects.create() so there are no duplicates.

get_or_create returns a tuple of two values: (object, created_boolean), which was why it's exercise, created. The created variable is then used for the counter for the terminal feedback.

We need a whole separate WorkoutExercise model instead of just adding the fields (exercises, sets, etc) to Workout model because then it'll allow the user to add only one exercise to the workout. The WorkoutExercise models uses. Think of the Workout as the 'title' and the WorkoutExercise as the bullet points beneath it. Each WorkoutExercise model is a different bullet point, same workout_id, different exercise_id. That's a many-to-many relationship with extra data attached to each pairing. There's no way to represent "many exercises per workout, each with unique numbers" using flat fields on Workout alone.

In forms.py, `inlineformset_factory(ParentModel, ChildModel, ...)` builds a set of forms for the child model (WorkoutExercise), all linked to one parent instance (Workout). It requires that WorkoutExercise has a ForeignKey to Workout (which it does).
- can_delete=True : adds a checkbox to each row so users can mark existing entries for deletion (useful when editing a workout later, not as relevant on initial creation).

In the templates, formset.management_form is used by the formset to manage the collection of forms contained in the formset. It is used to keep track of how many form instances are being displayed.

### Search Feature on <Select> Drop-Down 
Using select2 for an in-browser searchable <select>. Select2 replaces the plain <select> with a JS-enhanced dropdown that has a built-in search feature inside the dropdown itself. 

To use Select2:
1) in the WorkoutExerciseFormSet, add a widget for the exercise, where each exercise drop-down widget has the Select2 feature: 
    `'exercise': Select(attrs={'class': 'exercise-select'})`
2) In the add_workout.html template, in the <head>, add:
    ```html
        <link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
        <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>
    ```
3) Then, on the bottom of the html file, after the <form> tag (and <div> tag), add:
    ```html
        <script>
            $(document).ready(function() {
                $('.exercise-select').select2({
                    placeholder: 'Search for an exercise...',
                    width: '100%'
                });
            });
        </script>
    ```

### Loading the exercise.json file
To load the json file, we need to create the file within two folders, management and commands. So the file path should look something like this: ../yourApp/management/commands.
This is required because Django's command-discovery system works by scanning a fixed, predictable path inside every installed app. So, when you run `python manage.py load_exercises`, it doesn't go through your entire project files, just looking for the apps listed in INSTALLED_APPS for a folder literally named management/commands/, and treats every .py file in there as a potential command.

Both management/__init__.py and management/commands/__init__.py are empty, but they're not optional files; they're what makes Python treat management/ and management/commands/ as packages (importable modules) rather than just plain folders.

Once this structure is created, Django auto registers load_exercises as a subcommand. BaseCommand (which your Command class inherits from) handles the argument-parsing plumbing (add_arguments), the stdout/stderr styling helpers (self.style.SUCCESS, etc.), and the actual dispatch logic — you just fill in handle() with what should happen when the command runs.

Django provides BaseCommand as a base class for us to subclass and create custom commands (similar to how we have an Exception base class that we can use to create custom exceptions in Python and Java). If you want to create another command, create another file under management/commands/.

Every command file must define a class literally named Command. Django's loader doesn't care what you name the file variable-wise inside — it specifically looks for a class called Command in each file, because that's the convention it's built around.

The command-line generation is fully automatic. The moment load_workouts.py exists in tracker/management/commands with a properly defined `class Command(BaseCommand)`, Django's command-discovery logic (which runs every time you invoke manage.py) picks it up automatically.

### Dynamically add Exercise Rows to the formset
We want user to be able to add more exercise rows (since right now, there's only a fixed amoutn of exercises they can choose). To do this, we use Javascript in the templates. Underneath the form tag, we add a script tag (used for client-side Javascript code). Here's the code to let users dynamically add repeated groups of form fields:
```js
document.getElementById('add-exercise-btn').addEventListener('click', function() {
    const formsetContainer = document.getElementById('exercise-rows');
    const totalFormsInput = document.querySelector('#id_workoutexercise_set-TOTAL_FORMS');

    const formIndex = parseInt(totalFormsInput.value);

    const templateHtml = document.getElementById('empty-form-template').innerHTML;
    const newFormHtml = templateHtml.replace(/__prefix__/g, formIndex);

    const newRow = document.createElement('div');
    newRow.innerHTML = newFormHtml;
    formsetContainer.appendChild(newRow);

    totalFormsInput.value = formIndex + 1;

    initExerciseSelect2(newRow);
});
```
- document.getElementById('add-exercise-btn').addEventListener('click',function() {}); : runs the whole block when the "+ Add Exercise" button is clicked.

- const formsetContainer = document.getElementById('exercise-rows'); : Grabs the container element where all the individual exercise form rows live.

- const totalFormsInput = document.querySelector('#id_workoutexercise_set-TOTAL_FORMS'); : track how many forms exist via a hidden management-form input named `<prefix>-TTOTAL_FORMS`. This grabs that hidden field; Django uses its value server-side to know how many rows to expect when the form is submitted.

- const formIndex = parseInt(totalFormsInput.value); : reads the current count and converts it to a number. This becomes the index for the new row (e.g., if there are already 3 exercise rows, indices 0-2, the new one will be index 3).
 
- const templateHtml = document.getElementById('empty-form-template').innerHTML; : Django's formset can render an "empyt form" template with __prefix__ as a placeholder instead of a real index (e.g. field names like workoutexercise_set-__prefix__-exercise). This grabs that raw HTML tempalte, usually hidden on the page for exactly this purpose.

- const newFormHtml = templateHtml.replace(/__prefix__/g, formIndex); : replaces every occurrence of __prefix__ with the actual new index number, turning the placeholder template into real, uniquely-named form fields (e.g. workoutexercise_set-3-exercise).

- const newRow = document.createElement('div');
    newRow.innerHTML = newFormHtml;
    formsetContainer.appendChild(newRow);

    --> Creates a new <div>, stuffs the generated HTML inside it, and appends that div to the container, so the new row now appears on the page.

- totalFormsInput.value = formIndex + 1; 
    --> Increments the hidden TOTAL_FORMS count so Django knows there's now one more form to expec ton submit. This is !important!; w/o it, Django's formset validation won't even look at the new row's fields.

- initExerciseSelect2(newRow);
    --> Calls a custom function to initialize a Select2 dropdown widget on the new row, because Select2 (and similar JS plugins) don't auto-apply to elements added after the initial page load; you have to manually re-run the init on new DOM nodes.

