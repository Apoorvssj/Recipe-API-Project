"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """patched_check is the mock version
        of check method(used to check database status) ,
        patched_check is only available because we
        used patch decorator to mock a method i.e. check"""
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        # calls our wait_for_db command and
        # execute the code in it.
        call_command('wait_for_db')

        # now check if our mock check method is called or not
        # with these parameters -> database=['default']
        patched_check.assert_called_once_with(databases=['default'])

    # only need to mock for this function, cuz we are gonna wait for few secs before checking for db again , but we dont want to that in our test cases otherwise it will slowdown our test suite. so we will replace sleep with our magic mock function using patch
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # instead of retunring a value , here
        # we need to raise exceptions when
        # database is not connected, for that side_effect
        # is used,which allows us to pass in various
        # different items that get handled differently
        # depending on their type
        # so for error it raises them , but for True it returns boolean True
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
