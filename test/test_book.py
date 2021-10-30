import pydantic
import pytest


#from openlibrary.plugins.importapi.import_validator import (import_validator,
#                                                            RequiredFieldError)

from Books.book import Author, Book, Publisher, SourceRecord
# from import_validator import import_validator, RequiredFieldError

#from __future__ import annotations

#from datetime import datetime
#from typing import Any, Optional

#from pydantic import BaseModel, validator


def test_author_no_parameters():
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        Author()  # Must provide a `name` parameter


def test_author_name_equals_empty_str():
    author = Author(name="")  # Empty string is allowed (for now)
    assert isinstance(author, Author)
    assert author.name == ""


def test_author_without_name_key():
    with pytest.raises(TypeError):
        Author("")  # `name =` is NOT optional


def test_author_name_is_correct():
    author = Author(name="Bob")
    assert isinstance(author, Author)
    assert author.name == "Bob"


def test_author_from_dict():
    author = Author(**{"name": "External Data"})
    assert isinstance(author, Author)
    assert author.name == "External Data"


def test_author_to_json():
    assert Author(name="Json Is Builtin").json() == '{"name": "Json Is Builtin"}'


# Book tests

valid_book = Book(title = "",
         source_records = [SourceRecord(record="record")],
         authors = [Author(name="Bob")],
         publishers = [Publisher(name="Bob's Publishing")],
         publish_date = None,
         author = "",
         publisher = "",
     )
 

def test_book_title():
    assert isinstance(valid_book, Book)
    assert valid_book.title == ""


def test_book_with_no_author():
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        Book(
            title = valid_book.title,
            source_records = valid_book.source_records,
            authors = [],
            publishers = valid_book.publishers,
            publish_date = valid_book.publish_date,
            # author = valid_book.author,  # <--
            publisher = valid_book.publisher,
        )


def test_book_with_no_source_records():
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        Book(
            title = valid_book.title,
            source_records = [],  # <--
            authors = valid_book.authors,
            publishers = valid_book.publishers,
            publish_date = valid_book.publish_date,
            author = valid_book.author,
            publisher = valid_book.publisher,
        )
 

def test_book_with_authors_instead_of_source_records():
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        Book(
            title = valid_book.title,
            source_records = valid_book.authors,  # <--
            authors = valid_book.authors,
            publishers = valid_book.publishers,
            publish_date = valid_book.publish_date,
            author = valid_book.author,
            publisher = valid_book.publisher,
        )

