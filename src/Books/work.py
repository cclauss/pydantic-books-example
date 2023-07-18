from __future__ import annotations

import requests
from pydantic import BaseModel  # , validator


class OlId(BaseModel):
    key: str


class OlType(BaseModel):
    type: str
    value: str


class Identifier(BaseModel):
    goodreads: list[str]
    librarything: list[str]


class Work(BaseModel):
    authors: list[OlId]
    classifications: dict
    contributions: list[str]
    covers: list[int]
    created: OlType
    first_sentence: OlType
    identifiers: Identifier
    isbn_10: list[str]
    isbn_13: list[str]
    key: str
    languages: list[OlId]
    last_modified: OlType
    latest_revision: int
    local_id: list[str]
    number_of_pages: int
    ocaid: str
    publish_date: str
    publishers: list[str]
    revision: int
    source_records: list[str]
    title: str
    type: OlId
    works: list[OlId]


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
    url = f"https://openlibrary.org/{new_olid}.json"
    print(f"Gathering data from {url}.")
    # NOTE: json.JSONDecodeError may be raised if the record cannot be found.
    return requests.get(url, timeout=10).json()


if __name__ == "__main__":  # https://openlibrary.org/works/OL19545135W.json
    # Create and Open Library Work from a dict returned from requests
    work = Work(**get_openlibrary_data("isbn/0140328726"))  # isbn/0425016013"
    print(work)

    print(f"\nLazy loading {len(work.authors)} authors...\n")
    for i, author_olid in enumerate(work.authors):
        work.authors[i] = get_openlibrary_data(author_olid.key)  # type: ignore
    print(work)

    print(f"\nLazy loading {len(work.languages)} languages...\n")
    for i, language_olid in enumerate(work.languages):
        work.languages[i] = get_openlibrary_data(language_olid.key)  # type: ignore
    print(work)

    # If is a bad idea to shadow a Python builtin like `type`
    # print(f"\nLazy loading the type...\n")
    # work.type = get_openlibrary_data(type.key)
    # print(work)
