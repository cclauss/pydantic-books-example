from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class Author(BaseModel):
    name: str


class Publisher(BaseModel):
    name: str


class SourceRecord(BaseModel):
    record: str


class Book(BaseModel):
    title: str
    source_records: list[SourceRecord]
    authors: list[Author]
    publishers: list[Publisher]
    publish_date: Optional[datetime]
    author: str
    publisher: str

    @validator('source_records', 'authors', 'publishers')
    def list_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('list must not be empty')
        return v


# doctests... to be run with `pytest --doctest-modules`


def doctest_author():
    """
    >>> Author()  # Must provide a `name` parameter
    Traceback (most recent call last):
      ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Author
    name
      field required (type=value_error.missing)
    >>> Author(name="")  # Empty string is allowed (for now)
    Author(name='')
    >>> Author("")  # `name =` is NOT optional
    Traceback (most recent call last):
      ...
    TypeError: __init__() takes 1 positional argument but 2 were given
    >>> Author(name="Bob")
    Author(name='Bob')
    >>> external_data = {"name": ""}
    >>> no_name = Author(**external_data)  # Create an Author from a dict
    >>> no_name
    Author(name='')
    >>> no_name.json()  # Pydantic has json.dumps() is builtin
    '{"name": ""}'
    """


def doctest_book():
    """
    >>> Book(
    ...     title = "",
    ...     source_records = [],
    ...     authors = [],
    ...     publishers = [],
    ...     publish_date = None,
    ...     author = "",
    ...     publisher = "",
    ... )
    Traceback (most recent call last):
      ...
    pydantic.error_wrappers.ValidationError: 3 validation errors for Book
    source_records
      list must not be empty (type=value_error)
    authors
      list must not be empty (type=value_error)
    publishers
      list must not be empty (type=value_error)
    >>> Book(
    ...     title = "",
    ...     source_records = [Author(name="Bob")],
    ...     authors = [Author(name="Bob")],
    ...     publishers = [Author(name="Bob")],
    ...     publish_date = None,
    ...     author = "",
    ...     publisher = "",
    ... )
    Traceback (most recent call last):
      ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Book
    source_records -> 0 -> record
      field required (type=value_error.missing)
    >>> Book(
    ...     title = "",
    ...     source_records = [SourceRecord(record="record")],
    ...     authors = [Author(name="Bob")],
    ...     publishers = [Publisher(name="Bob's Publishing")],
    ...     publish_date = None,
    ...     author = "",
    ...     publisher = "",
    ... )
    Book(title='', source_records=[SourceRecord(record='record')], authors=[Author(name='Bob')], publishers=[Publisher(name="Bob's Publishing")], publish_date=None, author='', publisher='')
    """

