"""
This file holds all the main tests
"""

from bodybuilder.builder import BodyBuilder as bodyBuilder


def test_query_no_field():

    result = bodyBuilder().query('match_all')

    expected_query = {
        'match_all': {}
    }

    assert result.getQuery() == expected_query


def test_exist_user():
    result = bodyBuilder().query('exists', 'user')

    expected_query = {
        'exists': {
            'field': 'user'
        }
    }

    assert result.getQuery() == expected_query


def test_filter_without_query():
    result = bodyBuilder() \
        .filter('term', 'user', 'kimchy') \
        .build()

    expected_query = {
        'query': {
            'bool': {
                'filter': {
                    'term': {
                        'user': 'kimchy'
                    }
                }
            }
        }
    }

    assert result == expected_query


def test_query_and_filter():
    result = bodyBuilder() \
        .query('exists', 'user') \
        .filter('term', 'user', 'kimchy')

    expected_query = {
        'exists': {
            'field': 'user'
        }
    }
    expected_filter = {
        "term": {
            "user": 'kimchy'
        }
    }

    assert result.getQuery() == expected_query
    assert result.getFilter() == expected_filter


def test_filtered_query():
    result = bodyBuilder() \
        .query('match', 'message', 'this is a test') \
        .filter('term', 'user', 'kimchy') \
        .build()

    expected_query = {
        'query': {
            'bool': {
                'must': {
                    'match': {
                        'message': 'this is a test'
                    }
                },
                'filter': {
                    'term': {
                        'user': 'kimchy'
                    }
                }
            }
        }
    }

    assert result == expected_query


def test_basic_sort():
    result = bodyBuilder().sort('timestamp').build()
    expected_query = {
        "sort": [
            {
                'timestamp': {
                    "order": 'asc'
                }
            }
        ]
    }
    assert result == expected_query


def test_advanced_sort():
    result = bodyBuilder() \
        .sort('A', 'desc') \
        .sort('B', 'desc') \
        .sort('A') \
        .build()
    expected_query = {
        "sort": [
            {
                "A": {
                    "order": "asc"
                }
            },
            {
                "B": {
                    "order": "desc"
                }
            }
        ]
    }
    assert result == expected_query
