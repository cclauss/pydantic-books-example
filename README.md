# Pydantic books example
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/cclauss/pydantic-books-example/main.svg)](https://results.pre-commit.ci/latest/github/cclauss/pydantic-books-example/main)

This repo contains my experiments with [Pydantic](https://pydantic-docs.helpmanual.io) data validation.  [`src/Books/book.py`](../src/Books/book.py) defines four classes: Author, Book, Publisher, SourceRecord followed by some Python doctests to show how those classes are validated by Pydantic.  [test/test_book.py](../test/test_book.py) defines Python unittests to prove how the those classes are validated by Pydantic.

The doctests and unittests can be run with:
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
