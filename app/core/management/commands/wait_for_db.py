"""
Django command to wait for the database to be available.
"""
import time

from psycopg2 import OperationalError as Psycopg2Error  # error psycopg2 throws when postgres is not ready

from django.db.utils import OperationalError  # error that django throws when database is not ready
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    # standard syntax - handle method gets called when we run our django command
    def handle(self, *args, **options):
        """Entrypoint for command."""
        # log something to the screen while our command is executing
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except(Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
