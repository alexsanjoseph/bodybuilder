"""
Main Builder Class and functions
"""
from collections import OrderedDict


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
        self.sorts = OrderedDict()
        self.misc = {}
        self.body = {}
        self.rawOptions = {}

    def _add_bool_struct(self):
        self.body['query'] = {
            'bool': {}
        }

    @staticmethod
    def create_generic_query(*args):
        query_dict = {
            args[0]: {}
        }
        if len(args) == 1:
            return query_dict

        if len(args) == 2:
            query_field, query_val = 'field', args[1]
        else:
            query_field, query_val = args[1], args[2]

        query_dict[args[0]] = {
            query_field: query_val
        }
        if len(args) == 4:
            for key, value in args[3].items():
                query_dict[args[0]][key] = value
        if len(args) > 4:
            raise IndexError("Too many arguments to query!")

        return query_dict

    @staticmethod
    def create_sort_query(sort_dict):
        return [{key: {'order': value}}for key, value in sort_dict.items()]

    def _add_queries_simple(self):
        self.body['query'] = self.create_generic_query(*self.queries[0])

    def _add_queries(self):
        if len(self.queries) == 0:
            return
        if len(self.queries) <= 1:
            filter_dict = self.create_generic_query(*self.queries[0])
            self.body['query']['bool']['must'] = filter_dict
        else:
            raise NotImplementedError

    def _add_filters(self):
        if len(self.filters) == 0:
            return
        if len(self.filters) <= 1:
            filter_dict = self.create_generic_query(*self.filters[0])
            self.body['query']['bool']['filter'] = filter_dict
        else:
            raise NotImplementedError

    def _add_or_filters(self):
        pass

    def _add_not_filters(self):
        pass

    def _add_sorts(self):
        if len(self.sorts) == 0:
            return
        sort_dict_list = self.create_sort_query(self.sorts)
        self.body['sort'] = sort_dict_list

    def _add_rawOptions(self):
        for key, value in self.rawOptions.items():
            self.body[key] = value

    def _add_misc(self):
        if self.misc.get('from'):
            self.body['from'] = self.misc.get('from')
        if self.misc.get('size'):
            self.body['size'] = self.misc.get('size')

    ######################

    def is_simple_query(self):
        if len(self.queries) != 1:
            return False
        if len(self.filters) + len(self.orFilters) + len(self.notFilters) != 0:
            return False
        return True

    def query_exists(self):
        if (
            len(self.queries)
            + len(self.filters)
            + len(self.orFilters)
            + len(self.notFilters)
                ) > 0:
            return True
        return False

    def query(self, *args):
        self.queries.append(args)
        return self

    def filter(self, *args):
        self.filters.append(args)
        return self

    def aggregation(self, *args):
        self.aggs.append(args)
        return self

    def sort(self, *args):
        if len(args) > 2:
            raise ValueError
        sort_type = 'asc' if len(args) == 1 else args[1]
        self.sorts[args[0]] = sort_type
        return self

    def from_(self, value):
        self.misc['from'] = value
        return self

    def size(self, value):
        self.misc['size'] = value
        return self

    def getQuery(self):
        if self.is_simple_query():
            return self.build()['query']
        else:
            return self.build()['query']['bool']['must']

    def rawOption(self, key, value):
        self.rawOptions[key] = value
        return self

    def getFilter(self):
        return self.build()['query']['bool']['filter']

    def build(self):
        if self.query_exists():
            if self.is_simple_query():
                self._add_queries_simple()
            else:
                self._add_bool_struct()
                self._add_queries()
                self._add_filters()
                self._add_or_filters()
                self._add_not_filters()
        self._add_sorts()
        self._add_rawOptions()
        self._add_misc()
        return self.body

