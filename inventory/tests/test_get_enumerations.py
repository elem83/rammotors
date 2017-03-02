# pylint: disable=missing-docstring, unused-argument, undefined-variable

from unittest.mock import patch

import pytest # pylint: disable=unused-import

from inventory.models import Enumeration
from inventory.management.commands.get_enumerations import Command
from inventory.tests.test_services import get_lookup_mock

pytestmark = pytest.mark.django_db # pylint: disable=invalid-name

@patch('inventory.services.lookup', side_effect=get_lookup_mock)
def test_fill_db_with_enumeration(mock_lookup):
    command = Command()
    command.handle()
    enum_len = len(Enumeration.objects.all())
    assert enum_len != 0, \
            "The database should not be empty"
    command.handle()
    enum_len2 = len(Enumeration.objects.all())
    assert enum_len == enum_len2, \
            "The database should not be empty"
