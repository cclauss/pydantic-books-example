from json import loads as json_loads

import pydantic
import pytest

from Books.book import Author, Book, Publisher, SourceRecord

# Author tests


def test_author_no_parameters():
    with pytest.raises(pydantic.ValidationError):
        Author()  # Must provide a `name` parameter


def test_author_without_name_key():
    with pytest.raises(TypeError):
        Author("Bob")  # `name =` is NOT optional


def test_author_name_equals_empty_str():
    with pytest.raises(pydantic.ValidationError):
        Author(name="")  # @validator() ensures that an empty string is not allowed


def test_author_name_is_correct():
    author = Author(name="Bob")
    assert isinstance(author, Author)
    assert author.name == "Bob"


def test_author_from_dict():
    author = Author(**{"name": "External Data"})
    assert isinstance(author, Author)
    assert author.name == "External Data"


def test_author_to_json():
    assert (
        Author(name="Json Is Builtin").model_dump_json() == '{"name":"Json Is Builtin"}'
    )


# Book tests

valid_book = Book(
    title="",
    source_records=[SourceRecord(record="record")],
    authors=[Author(name="Bob")],
    publishers=[Publisher(name="Bob's Publishing")],
    publish_date=None,
    author="",
    publisher="",
)


def test_book_title():
    assert isinstance(valid_book, Book)
    assert valid_book.title == ""


def test_book_with_no_author():
    with pytest.raises(pydantic.ValidationError):
        Book(
            title=valid_book.title,
            source_records=valid_book.source_records,
            authors=[],
            publishers=valid_book.publishers,
            publish_date=valid_book.publish_date,
            # author = valid_book.author,  # <--
            publisher=valid_book.publisher,
        )


def test_book_with_no_source_records():
    with pytest.raises(pydantic.ValidationError):
        Book(
            title=valid_book.title,
            source_records=[],  # <--
            authors=valid_book.authors,
            publishers=valid_book.publishers,
            publish_date=valid_book.publish_date,
            author=valid_book.author,
            publisher=valid_book.publisher,
        )


def test_book_with_authors_instead_of_source_records():
    with pytest.raises(pydantic.ValidationError):
        Book(
            title=valid_book.title,
            source_records=valid_book.authors,  # <--
            authors=valid_book.authors,
            publishers=valid_book.publishers,
            publish_date=valid_book.publish_date,
            author=valid_book.author,
            publisher=valid_book.publisher,
        )


# Json tests

valid_book_json = """{"title": "json",
    "source_records": [{"record": "record"}],
    "authors": [{"name": "Bob"}],
    "publishers": [{"name": "Bob\'s Publishing"}],
    "publish_date": null,
    "author": "",
    "publisher": ""}"""


def test_book_json_title():
    book = Book(**json_loads(valid_book_json))
    assert isinstance(book, Book)
    assert book.title == "json"


invalid_book_json = """{"title": "json",
    "source_records": [{"record": "record"}],
    "authors": [{"name": ""}],
    "publishers": [{"name": "Bob\'s Publishing"}],
    "publish_date": null,
    "author": "",
    "publisher": ""}"""


def test_book_json_invalid_author_has_no_name():
    with pytest.raises(pydantic.ValidationError):
        Book(**json_loads(invalid_book_json))


invalid_book_json = """{"title": "json",
    "source_records": [{"record": "record"}],
    "authors": [{"name": "Bob"}, {"something else": "Bob"}],
    "publishers": [{"name": "Bob\'s Publishing"}],
    "publish_date": null,
    "author": "",
    "publisher": ""}"""


def test_book_json_invalid_second_author():
    with pytest.raises(pydantic.ValidationError):
        Book(**json_loads(invalid_book_json))
