[![PyPI download total](https://img.shields.io/pypi/dm/bodybuilder)](https://pypi.org/project/bodybuilder/)
[![License](https://img.shields.io/pypi/l/bodybuilder)](https://pypi.org/project/bodybuilder/)
[![License](https://img.shields.io/pypi/v/builder)](https://pypi.org/project/bodybuilder/)


# bodybuilder
An (almost!) drop in replacement in python of the [Elasticsearch Bodybuilder Package on NPM](https://github.com/danpaz/bodybuilder)

The API has been designed to be as close to the original package.

Also, you can use https://bodybuilder.js.org/ to test your constructions with minor changes described below:

## Variations
- `from` -> `from_` because `from` is a python keyword
- need `\` new-line indicator for multi line incantations in python which is not necessary in JS
- individual Filter/Query/Aggregations classes not implemented (shouldn't affect user)
- lambda functions instead of anonymous functions (Duh!)


# Requirements

Python3.6+

# Installation

## Pip install

1. `pip3 install bodybuilder`

## Install from source

1. Clone package locally
2. Go to the root directory
2. `python3 setup.py install`

# Usage

```python
from bodybuilder import BodyBuilder as bodyBuilder
bodyBuilder().query("a", "b", "c").build()
```

```
{'query': {'a': {'b': 'c'}}}
```

# Not Implemented

## To be implemented
- minimum_should_match query and filter
- aggregation metadata

## No plans to implement

- Complicated multi sort
- `clone` method (users can use `copy.deepcopy()` if required)
- `orQuery`, `andQuery`, `notQuery` which has been deprecated n favor of `bool` method

# Credits

Thanks to [Danpaz](https://github.com/danpaz) and [contributors of the original package](https://github.com/danpaz/bodybuilder#contributors) for the original package from which I have liberally copied (with his permission!)
