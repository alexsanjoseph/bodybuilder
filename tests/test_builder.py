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

    def test__basic_filter(self):
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

    def test__not_filter(self):
        result = bodyBuilder() \
            .notFilter('term', 'user', 'kimchy') \
            .build()

        expected_query = {
            'query': {
                'bool': {
                    'must_not': [{
                        'term': {
                            'user': 'kimchy'
                        }
                    }]
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
                   .query('range', 'obj1.count',
                          {
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
            .query('nested', 'path', 'comments',
                   {
                       'score_mode': 'max'
                   },
                   lambda q: q
                   .query('match', 'comments.name', 'john')
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

    def test__constant_score(self):
        result = bodyBuilder() \
            .filter('constant_score',
                    lambda f: f.filter('term', 'field', 'value')
                    )

        expected_query = {
            'constant_score': {
                'filter': {
                    'term': {
                        'field': 'value'
                    }
                }
            }
        }

        assert result.getFilter() == expected_query

    def test__bigass_query(self):
        result = bodyBuilder() \
            .query('constant_score',
                   lambda q: q
                   .orFilter('term', 'created_by.user_id', 'abc')
                   .orFilter(
                       'nested', 'path', 'doc_meta',
                       lambda q1: q1.
                       query(
                            'constant_score',
                            lambda q2: q2
                            .filter('term',
                                    'doc_meta.user_id',
                                    'abc')
                           )
                   )
                   .orFilter('nested', 'path', 'tests',
                             lambda q1: q1
                             .query('constant_score',
                                    lambda q2: q2
                                    .filter(
                                        'term',
                                        'tests.created_by.user_id',
                                        'abc')
                                    )
                             )
                   )

        expected_query = {
            "constant_score": {
                "query": {  # originally filter?
                    "bool": {
                        "should": [
                            {
                                "term": {
                                    "created_by.user_id": "abc"
                                }
                            },
                            {
                                "nested": {
                                    "path": "doc_meta",
                                    "query": {
                                        "constant_score": {
                                            "filter": {
                                                "term": {
                                                    "doc_meta.user_id": "abc"
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "nested": {
                                    "path": "tests",
                                    "query": {
                                        "constant_score": {
                                            "filter": {
                                                "term": {
                                                    "tests.created_by.user_id": "abc"  # noqa 501
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }

        assert result.getQuery() == expected_query

    def test__query_filter_aggs(self):
        result = bodyBuilder() \
            .query('match', 'message', 'this is a test') \
            .filter('term', 'user', 'kimchy') \
            .filter('term', 'user', 'herald') \
            .orFilter('term', 'user', 'johnny') \
            .notFilter('term', 'user', 'cassie') \
            .aggregation('terms', 'user') \
            .build()

        expected_query = {
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "message": "this is a test"
                        }
                    },
                    "filter": [{
                        "term": {
                            "user": "kimchy"
                        }
                    }, {
                        "term": {
                            "user": "herald"
                        }
                    }],
                    "should": [{
                        "term": {
                            "user": "johnny"
                        }
                    }],
                    "must_not": [{
                        "term": {
                            "user": "cassie"
                        }
                    }]
                }
            },
            "aggs": {
                "agg_terms_user": {
                    "terms": {
                        "field": "user"
                    }
                }
            }
        }

        assert result == expected_query

    def test__dynamic_filter(self):
        result = bodyBuilder() \
            .filter('constant_score',
                    lambda f: f.filter('term', 'user', 'kimchy')) \
            .filter('term', 'message', 'this is a test') \
            .build()

        expected_query = {
            "query": {
                "bool": {
                    "filter": [
                        {
                            "constant_score": {
                                "filter": {
                                    "term": {
                                        "user": "kimchy"
                                    }
                                }
                            }
                        },
                        {
                            "term": {
                                "message": "this is a test"
                            }
                        }
                    ]

                }
            }
        }
        assert result == expected_query

    def test__complex_dynamic_filter(self):
        result = bodyBuilder() \
            .orFilter('bool',
                      lambda f: f
                      .filter('terms', 'tags', ['Popular'])
                      .filter('terms', 'brands', ['A', 'B'])
                      ) \
            .orFilter('bool',
                      lambda f: f
                      .filter('terms', 'tags', ['Emerging'])
                      .filter('terms', 'brands', ['C'])
                      ) \
            .orFilter('bool',
                      lambda f: f
                      .filter('terms', 'tags', ['Rumor'])
                      .filter('terms', 'companies', ['A', 'C', 'D'])
                      ) \
            .build()
        expected_query = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "bool": {
                                "filter": [{
                                    "terms": {
                                        "tags": ["Popular"]
                                    }
                                }, {
                                    "terms": {
                                        "brands": ["A", "B"]
                                    }
                                }]
                            }
                        },
                        {
                            "bool": {
                                "filter": [{
                                    "terms": {
                                        "tags": ["Emerging"]
                                    }
                                }, {
                                    "terms": {
                                        "brands": ["C"]
                                    }
                                }]
                            }
                        },
                        {
                            "bool": {
                                "filter": [
                                    {
                                        "terms": {
                                            "tags": ["Rumor"]
                                        }
                                    },
                                    {
                                        "terms": {
                                            "companies": ["A", "C", "D"]
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }
        assert result == expected_query

    @pytest.mark.skip
    def test__minimum_should_match(self):

        result = bodyBuilder() \
            .orFilter('term', 'user', 'kimchy') \
            .orFilter('term', 'user', 'tony') \
            .filterMinimumShouldMatch(2) \
            .build()

        expected_query = {
            "query": {
                "bool": {
                    "should": [{
                        "term": {
                            "user": "kimchy"
                        }
                    }, {
                        "term": {
                            "user": "tony"
                        }
                    }],
                    "minimum_should_match": 2
                }
            }
        }

        assert result == expected_query
