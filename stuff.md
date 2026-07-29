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

# Edit/Delete Button


