# Pydantic books example
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/cclauss/pydantic-books-example/main.svg)](https://results.pre-commit.ci/latest/github/cclauss/pydantic-books-example/main)

This repo contains my experiments with [Pydantic](https://pydantic-docs.helpmanual.io) data validation.  [`src/Books/book.py`](../../tree/main/src/Books/book.py) defines four classes: `Author`, `Book`, `Publisher`, `SourceRecord` followed by some Python doctests to show how those classes are validated by Pydantic.  This data validation is mostly handled via Pydantic's verifying type hint compliance at runtime and type conversion where needed.

```python
from datetime import date
from typing import Optional

from pydantic import BaseModel, validator


class Book(BaseModel):
    title: str
    source_records: list[SourceRecord]
    authors: list[Author]
    publishers: list[Publisher]
    publish_date: Optional[date]
    author: str
    publisher: str

    @validator("source_records", "authors", "publishers")
    def list_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("list must not be empty")
        return v
```
Given `Book(requests.get(url).json())` please provide easy to understand error messages that:
1. The `title` is an empty string.
2. The `publishers` list is empty.
3. The third `SourceRecord` does not contain the required `record` field.
4. The fourth `Author` has a `name` that is an empty string.

Just by providing the data classes mentioned above, Pydantic can quickly find all of those problems and deliver detailed end-user-ready error messages.

I am impressed with the detailed exceptions Pydantic raises which pinpoint where bad data is even in nested data structures.  The code also demonstrates the use of `@validator` functions to ensure that lists or strings are not empty, etc.  For dates, it could also be interesting to wire an `@validator` function to [one of the datetime for humans libraries](https://github.com/kennethreitz/maya#-what-about-delorean-arrow--pendulum) to coerce strings like "October 2021" into valid datetimes.

[`test/test_book.py`](../../tree/main/test/test_book.py) defines Python unittests to prove how the those classes are validated by Pydantic. Both the doctests and unittests can be run with:
`pytest --doctest-modules .`
```
================================== test session starts ==================================
platform darwin -- Python 3.9.7, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
rootdir: /Users/cclauss/Python/import_validator/pydantic-books-example
collected 16 items

src/Books/book.py ...                                                             [ 18%]
test/test_book.py .............                                                   [100%]

================================== 16 passed in 0.04s ===================================
```
