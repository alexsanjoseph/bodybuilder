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
        self.minimumShouldMatch = {}

    def _add_bool_struct(self):
        self.body['query'] = {
            'bool': {}
        }

    @staticmethod
    def _add_nested_function_query(query_dict, nested_function, query_name):
        if nested_function is None:
            return query_dict
        built_class = nested_function(BodyBuilder())
        if len(built_class.filters) > 0:
            nested_query = built_class.getFilter()
            query_dict[query_name]['filter'] = nested_query
        else:
            nested_query = built_class.getQuery()
            query_dict[query_name]['query'] = nested_query
        return query_dict

    @staticmethod
    def _create_empty_query_dict(query_name):
        return {
            query_name: {}
        }

    @staticmethod
    def _get_query_field_value(args_list):
        if len(args_list) == 2:
            query_field, query_val = 'field', args_list[1]
        else:
            query_field, query_val = args_list[1], args_list[2]
        return query_field, query_val

    @staticmethod
    def create_generic_query(*args):
        args_list = list(args)
        query_name = args_list[0]
        query_dict = BodyBuilder._create_empty_query_dict(query_name)

        nested_function = args_list.pop() if callable(args_list[-1]) else None

        if len(args_list) > 1:
            query_field, query_val = BodyBuilder._get_query_field_value(args_list)

            query_dict[query_name] = {
                query_field: query_val
            }

            if len(args_list) == 4:
                for key, value in args_list[3].items():
                    query_dict[args_list[0]][key] = value

            if len(args_list) > 4:
                raise IndexError("Too many arguments to query!")

        query_dict = BodyBuilder._add_nested_function_query(
            query_dict, nested_function, query_name)

        return query_dict

    @staticmethod
    def _get_query_field_dict_aggs(args_list):
        return {'field': args_list[1]} if type(args_list[1]) is str else {}

    @staticmethod
    def _get_aggs_options(args_list, query_field_dict):
        additional_options = [x for x in args_list if type(x) is dict]
        return {key: value for d in (additional_options + [query_field_dict])
                for key, value in d.items()}

    @staticmethod
    def _get_aggs_query_name(args_list, query_field, query_type):
        query_name_candidates = [x for x in args_list[2:] if type(x) is str]

        if len(query_name_candidates) > 0:
            query_name = query_name_candidates[0]
        else:
            if len(query_field) == 0:
                raise ValueError("Query name should be provided \
                                  if query field is empty")
            query_name = f"agg_{query_type}_{list(query_field.values())[0]}"
        return query_name

    @staticmethod
    def _add_nested_function_aggs(query_dict, nested_function, query_name):
        if nested_function is None:
            return query_dict
        nested_aggs_query = nested_function(BodyBuilder()).getAggregations()
        query_dict[query_name]['aggs'] = nested_aggs_query
        return query_dict

    @staticmethod
    def create_aggs_query(*args):

        if len(args) <= 1:
            raise IndexError("Too Few arguments for aggregation query")
        args_list = list(args)

        nested_function = args_list.pop() if callable(args_list[-1]) else None

        query_type = args_list[0]
        query_field = BodyBuilder._get_query_field_dict_aggs(args_list)
        all_options = BodyBuilder._get_aggs_options(args_list, query_field)
        query_name = BodyBuilder._get_aggs_query_name(args_list, query_field, query_type)  # noqa E501

        query_dict = {
            query_name: {
                query_type: all_options
            }
        }

        query_dict = BodyBuilder._add_nested_function_aggs(
            query_dict, nested_function, query_name)

        return query_dict

    @staticmethod
    def create_sort_query(sort_dict):
        return [{
            key: {
                'order': value
            }
        } for key, value in sort_dict.items()]

    def _add_queries_simple(self):
        self.body['query'] = self.create_generic_query(*self.queries[0])

    def _add_bool_queries(self, query_type, name):
        if len(getattr(self, query_type)) == 0:
            return
        always_array_types = ['orFilters', 'notFilters']
        if len(getattr(self, query_type)) == 1 and query_type not in always_array_types:
            bool_dict = self.create_generic_query(*getattr(self, query_type)[0])
            self.body['query']['bool'][name] = bool_dict
        else:
            bool_list = [self.create_generic_query(*x) for x in getattr(self, query_type)]
            self.body['query']['bool'][name] = bool_list

    def _add_aggs(self):
        if len(self.aggs) == 0:
            return
        if len(self.aggs) <= 1:
            aggs_dict = self.create_aggs_query(*self.aggs[0])
            self.body['aggs'] = aggs_dict
        else:
            raise NotImplementedError

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

    def orFilter(self, *args):
        self.orFilters.append(args)
        return self

    def notFilter(self, *args):
        self.notFilters.append(args)
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
        return self.build()['query']

    def getFilter(self):
        return self.build()['query']['bool']['filter']

    def getAggregations(self):
        return self.build()['aggs']

    def rawOption(self, key, value):
        self.rawOptions[key] = value
        return self

    def queryMinimumShouldMatch(self, value):
        self.minimumShouldMatch['query'] = value
        return self

    def filterMinimumShouldMatch(self, value):
        self.minimumShouldMatch['filter'] = value
        return self

    def add_query_details(self):
        if self.is_simple_query():
            self._add_queries_simple()
        else:
            self._add_bool_struct()
            self._add_bool_queries('queries', 'must')
            self._add_bool_queries('filters', 'filter')
            self._add_bool_queries('orFilters', 'should')
            self._add_bool_queries('notFilters', 'must_not')

    def build(self):
        if self.query_exists():
            self.add_query_details()
        self._add_sorts()
        self._add_rawOptions()
        self._add_misc()
        self._add_aggs()
        return self.body
