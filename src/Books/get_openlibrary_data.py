"""
Get book and author data from https://openlibrary.org

ISBN: https://en.wikipedia.org/wiki/International_Standard_Book_Number
"""

# import json

import requests


def get_openlibrary_data(olid: str) -> dict:
    """
    Given an 'isbn/0140328726', return book data from Open Library as a Python dict.
    Given an '/authors/OL34184A', return authors data as a Python dict.
    This code must work for olids with or without a leading slash ('/').

    # Comment out doctests if they take too long or have results that may change
    # >>> get_openlibrary_data(olid='isbn/0140328726')  # doctest: +ELLIPSIS
    {'publishers': ['Puffin'], 'number_of_pages': 96, 'isbn_10': ['0140328726'], ...
    # >>> get_openlibrary_data(olid='/authors/OL7353617A')  # doctest: +ELLIPSIS
    {'name': 'Adrian Brisku', 'created': {'type': '/type/datetime', ...
    """
    new_olid = olid.strip().strip("/")  # Remove leading/trailing whitespace & slashes
    if new_olid.count("/") != 1:
        raise ValueError(f"{olid} is not a valid Open Library olid")
    # NOTE: json.JSONDecodeError may be raised if the record cannot be found.
    return requests.get(f"https://openlibrary.org/{new_olid}.json", timeout=10).json()


def build_data_class(data, depth=1, sort_keys=True) -> None:
    """
    A very poor man's version of https://pypi.org/project/datamodel-code-generator
    Semi-automate the process of building data classes from json data.
    See docstring at the bottom of the file for output.
    """
    indent = " " * depth * 4
    if sort_keys:
        data = dict(sorted(data.items()))  # sort keys in alphabetic order
    for key, value in data.items():
        if key == "type":  # https://github.com/koxudaxi/datamodel-code-generator#600
            key = "type_"
        s = f"{indent}{key}: {type(value).__name__}"  # ocaid: str
        if value and isinstance(value, list):
            print(f"{s}[{type(value[0]).__name__}]")  # covers: list[int]
            if isinstance(value[0], dict):
                build_data_class(value[0], depth + 1)
        else:
            print(s)
            if value and isinstance(value, dict):
                build_data_class(value, depth + 1)


if __name__ == "__main__":  # https://openlibrary.org/works/OL19545135W.json
    data = get_openlibrary_data("isbn/0140328726")  # isbn/0425016013")
    # print(data)
    # print(json.dumps(data, indent=4))
    print("\n\nclass Work:")
    build_data_class(data)

"""
class Work:
    authors: list[dict]
        key: str
    classifications: dict
    contributions: list[str]
    covers: list[int]
    created: dict
        type_: str
        value: str
    first_sentence: dict
        type_: str
        value: str
    identifiers: dict
        goodreads: list[str]
        librarything: list[str]
    isbn_10: list[str]
    isbn_13: list[str]
    key: str
    languages: list[dict]
        key: str
    last_modified: dict
        type_: str
        value: str
    latest_revision: int
    local_id: list[str]
    number_of_pages: int
    ocaid: str
    publish_date: str
    publishers: list[str]
    revision: int
    source_records: list[str]
    title: str
    type_: dict
        key: str
    works: list[dict]
        key: str
"""
