import pytest
from unittest.mock import patch
from main import *

class Tests:
    @staticmethod
    def test_sanity_check():
        expected = True
        actual = True
        assert actual == expected