"""
This file holds all the main tests
"""
import pytest

from bodybuilder.builder import BodyBuilder as bodyBuilder


class TestBodyBuilder:

    def test__query_no_field(self):
        result = bodyBuilder().query('match_all')

        expected_query = {
            'match_all': {}
        }

        assert result.getQuery() == expected_query

    def test__exist_user(self):
        result = bodyBuilder().query('exists', 'user')

        expected_query = {
            'exists': {
                'field': 'user'
            }
        }

        assert result.getQuery() == expected_query

    def test__filter_without_query(self):
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

    def test__query_and_filter(self):
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

        assert result.build()['query']['bool']['must'] == expected_query
        assert result.build()['query']['bool']['filter'] == expected_filter

    def test__filtered_query(self):
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

    def test__multiple_filters(self):
        result = bodyBuilder() \
            .filter('range', 'count', {'gt': 5}) \
            .filter('term', 'a') \
            .build()

        expected_query = {
            'query': {
                'bool': {
                    'filter': [
                        {
                            'range': {
                                'count': {
                                    'gt': 5
                                }
                            }
                        },
                        {
                            'term': {
                                'field': "a"
                            }
                        }
                    ]
                }
            }
        }

        assert expected_query == result

    def test__basic_sort(self):
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

    def test__advanced_sort(self):
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

    def test__from(self):
        result = bodyBuilder() \
            .from_(10) \
            .build()

        expected_query = {
            "from": 10
        }

        assert result == expected_query

    def test__size(self):
        result = bodyBuilder() \
            .size(10) \
            .build()

        expected_query = {
            "size": 10
        }

        assert result == expected_query

    def test__rawOption(self):
        result = bodyBuilder() \
            .rawOption('a', {'b': 'c'}) \
            .build()

        expected_query = {
            'a': {
                'b': 'c'
            }
        }

        assert result == expected_query

    def test__query_key_value(self):
        result = bodyBuilder().query('term', 'user', 'kimchy')

        expected_query = {
            'term': {
                'user': 'kimchy'
            }
        }

        assert result.getQuery() == expected_query

    def test__query_field_object(self):
        result = bodyBuilder() \
            .query('range', 'date', {'gt': 'now-1d'})

        expected_query = {
            'range': {
                'date': {
                    'gt': 'now-1d'
                }
            }
        }

        assert result.getQuery() == expected_query

    def test__query_with_more_options(self):
        result = bodyBuilder() \
            .query('geo_distance',
                   'point',
                   {
                       'lat': 40,
                       'lon': 20
                   },
                   {
                       'distance': '12km'
                   }
                   )
        expected_query = {
            'geo_distance': {
                'point': {
                    'lat': 40,
                    'lon': 20
                },
                'distance': '12km'
            }
        }

        assert result.getQuery() == expected_query

    def test__aggregation_few_arguments(self):
        with pytest.raises(IndexError) as e:
            bodyBuilder().aggregation().build()
        assert "Too Few arguments for aggregation query" in str(e.value)

        with pytest.raises(IndexError) as e:
            bodyBuilder().aggregation("a").build()
        assert "Too Few arguments for aggregation query" in str(e.value)

    def test__nested_aggregations(self):
        result = bodyBuilder() \
            .aggregation(
                "a", "b", {"c": "d"}, "e",
                lambda x: x.aggregation(
                    "f", "g",
                    lambda y: y.aggregation("h", "i", "j"))) \
            .build()
        expected_query = {
            "aggs": {
                "e": {
                    "a": {
                        "field": "b",
                        "c": "d"
                    },
                    "aggs": {
                        "agg_f_g": {
                            "f": {
                                "field": "g"
                            },
                            "aggs": {
                                "j": {
                                    "h": {
                                        "field": "i"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        assert result == expected_query

    def test__nested_queries(self):
        result = bodyBuilder() \
            .query('nested', 'path', 'obj1',
                   lambda q: q.query('match', 'obj1.color', 'blue')
                   )

        expected_query = {
            'nested': {
                'path': 'obj1',
                'query': {
                    'match': {
                        'obj1.color': 'blue'
                    }
                }
            }
        }

        assert result.getQuery() == expected_query

    def test__nest_bool_merged_queries(self):
        result = bodyBuilder() \
            .query('nested', 'path', 'obj1',
                   {
                       'score_mode': 'avg'
                   },
                   lambda q: q
                   .query('match', 'obj1.name', 'blue')
                   .query('range', 'obj1.count', {
                       'gt': 5
                   }
                          )
                   )

        expected_query = {
            'nested': {
                'path': 'obj1',
                'score_mode': 'avg',
                'query': {
                    'bool': {
                        'must': [
                            {
                                'match': {
                                    'obj1.name': 'blue'
                                }
                            },
                            {
                                'range': {
                                    'obj1.count': {
                                        'gt': 5
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }

        assert result.getQuery() == expected_query

    def test__chained_nested(self):
        result = bodyBuilder() \
            .query('match', 'title', 'eggs') \
            .query('nested', 'path', 'comments', {
            'score_mode': 'max'
        },
                   lambda q: q \
                   .query('match', 'comments.name', 'john') \
                   .query('match', 'comments.age', 28)
                   )

        expected_query = {
            'bool': {
                'must': [
                    {
                        'match': {
                            'title': 'eggs'
                        }
                    },
                    {
                        'nested': {
                            'path': 'comments',
                            'score_mode': 'max',
                            'query': {
                                'bool': {
                                    'must': [
                                        {
                                            'match': {
                                                'comments.name': 'john'
                                            }
                                        },
                                        {
                                            'match': {
                                                'comments.age': 28
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    }
                ]
            }
        }

        assert result.getQuery() == expected_query
