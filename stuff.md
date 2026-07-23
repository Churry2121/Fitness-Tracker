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

