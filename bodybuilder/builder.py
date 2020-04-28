"""
Main Builder Class and functions
"""


class BodyBuilder:

    """
    Builder Class which creates the queries
    """

    def __init__(self):
        self.query_dict = None

    def query(self, query_type):

        """
        Add Query to class
        """
        if query_type == "match_all":
            self.query_dict = {
                'match_all': {}
            }
        return self

    def get_query(self):
        """
        Return Query JSON
        """
        return self.query_dict
