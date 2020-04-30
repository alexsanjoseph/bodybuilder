"""
This file holds all the main tests
"""

from bodybuilder.builder import BodyBuilder as BB


def test_query_no_field():

    result = BB().query('match_all')

    expected_query = {
        'match_all': {}
    }

    assert result.get_query() == expected_query


def test_exist_user():
    result = BB().query('exists', 'user')

    expected_query = {
        'exists': {
            'field': 'user'
        }
    }

    assert result.get_query() == expected_query
