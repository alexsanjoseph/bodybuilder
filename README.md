# bodybuilder
An (almost!) drop in replacement of the Elasticsearch Bodybuilder Package on NPM

# Variations
- `from` -> `from_` because `from` is a python keyword
- individual Filter/Query/Aggregations classes not implemented (shouldn't affect user)
- lambda functions instead of anonymous functions (Duh!)

# Not Implemented
- Complicated multi sort
- `clone` method (users can use `copy.deepcopy()` if required)
- `orQuery`, `andQuery`, `notQuery` which has been deprecated n favor of `bool` method

