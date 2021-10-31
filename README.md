# Pydantic books example
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/cclauss/pydantic-books-example/main.svg)](https://results.pre-commit.ci/latest/github/cclauss/pydantic-books-example/main)

This repo contains my experiments with [Pydantic](https://pydantic-docs.helpmanual.io) data validation.  [`src/Books/book.py`](../../tree/main/src/Books/book.py) defines four classes: Author, Book, Publisher, SourceRecord followed by some Python doctests to show how those classes are validated by Pydantic.  Data validation is mostly handled via Pydantic's verifying type hint compliance and type conversion at runtime.

I am impressed with the detailed exceptions Pydantic raises which pinpoint where the bad data is even in nested data structures.  The code also demonstrates the use of `@validator` functions to ensure that lists or strings are not empty, etc.

[`test/test_book.py`](../../tree/main/test/test_book.py) defines Python unittests to prove how the those classes are validated by Pydantic. Both the doctests and unittests can be run with:
% `pytest --doctest-modules .`
```
============================= test session starts ==============================
platform linux -- Python 3.10.0, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
rootdir: /home/runner/work/pydantic-books-example/pydantic-books-example
collected 12 items

src/Books/book.py ..                                                     [ 16%]
test/test_book.py ..........                                             [100%]

============================== 12 passed in 0.29s ==============================
```
