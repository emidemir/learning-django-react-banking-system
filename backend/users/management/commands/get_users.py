from django.core.management.base import BaseCommand

# THIS FILE IS CURRENTLY EMPTY. I CREATED IN CASE I NEED IT LATER

class Command(BaseCommand):
    help="Gets all the users in the project, and prints them"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="Allows you to specify the name of the user")
        parser.add_argument('--loud', action='store_true', help="Prints the message in uppercase")

    def handle(self, *args, **options):
        name = options['name']
        loud = options['loud']

        greeting = f"Hello {name}! Welcome!"

        if loud:
            greeting = greeting.upper()
        
        self.stdout.write(greeting)