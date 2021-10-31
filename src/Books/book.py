from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class Author(BaseModel):
    name: str

    @validator("name")
    def author_name_must_not_be_an_empty_string(cls, v):
        if not v:
            raise ValueError("name must not be an empty string")
        return v


class Publisher(BaseModel):
    name: str

    @validator("name")
    def publisher_name_must_not_be_an_empty_string(cls, v):
        if not v:
            raise ValueError("name must not be an empty string")
        return v


class SourceRecord(BaseModel):
    record: str

    @validator("record")
    def record_must_not_be_an_empty_string(cls, v):
        if not v:
            raise ValueError("record must not be an empty string")
        return v


class Book(BaseModel):
    title: str
    source_records: list[SourceRecord]
    authors: list[Author]
    publishers: list[Publisher]
    publish_date: Optional[datetime]
    author: str
    publisher: str

    @validator("source_records", "authors", "publishers")
    def list_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("list must not be empty")
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
    >>> Author(name="")  # @validator() ensures that an empty string is not allowed
    Traceback (most recent call last):
      ...
    pydantic.error_wrappers.ValidationError: 1 validation error for Author
    name
      name must not be an empty string (type=value_error)
    >>> Author("")  # `name =` is NOT optional
    Traceback (most recent call last):
      ...
    TypeError: ...__init__() takes 1 positional argument but 2 were given
    >>> Author(name="Bob")
    Author(name='Bob')
    >>> external_data = {"name": "From Dict"}
    >>> from_dict = Author(**external_data)  # Create an Author from a dict
    >>> from_dict
    Author(name='From Dict')
    >>> from_dict.json()  # Pydantic has json.dumps() is builtin
    '{"name": "From Dict"}'
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
