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
                    'instructions': entry.get('instructions', {}).get('en', ''),
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
