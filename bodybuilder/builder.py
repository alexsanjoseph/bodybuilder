"""
Main Builder Class and functions
"""


class BodyBuilder:

    """
    Builder Class which creates the queries
    """

    def __init__(self):
        self.queries = []
        self.filters = []
        self.orFilters = []
        self.notFilters = []
        self.aggs = []
        self.body = {}

    def _add_queries_simple(self):
        simple_query = self.queries[0]
        query_dict = {
            simple_query[0]: {}
        }
        if simple_query[1] is not None:
            query_dict[simple_query[0]] = {
                simple_query[2]: simple_query[1]
            }
        self.body['query'] = query_dict

    def _add_queries(self):
        pass

    def _add_filters(self):
        pass

    def _add_or_filters(self):
        pass

    def _add_not_filters(self):
        pass

    def query(self, query_type, query_val=None, query_field='field'):
        self.queries.append((query_type, query_val, query_field))
        return self

    def filter(self, type, field, value):
        pass

    def is_simple_query(self):
        if len(self.queries) != 1:
            return False
        if len(self.filters) + len(self.orFilters) + len(self.notFilters) != 0:
            return False
        return True

    def build(self):
        if self.is_simple_query():
            self._add_queries_simple()
        else:
            self._add_queries()
            self._add_filters()
            self._add_or_filters()
            self._add_not_filters()
        return self.body

    def get_query(self):
        return self.build()['query']
