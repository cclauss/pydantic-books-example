from __future__ import annotations

from datetime import date

from pydantic import BaseModel, field_validator


class Author(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def author_name_must_not_be_an_empty_string(cls, v):
        if not v:
            raise ValueError("name must not be an empty string")
        return v


class Publisher(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def publisher_name_must_not_be_an_empty_string(cls, v):
        if not v:
            raise ValueError("name must not be an empty string")
        return v


class SourceRecord(BaseModel):
    record: str

    @field_validator("record")
    @classmethod
    def record_must_not_be_an_empty_string(cls, v):
        if not v:
            raise ValueError("record must not be an empty string")
        return v


class Book(BaseModel):
    title: str
    source_records: list[SourceRecord]
    authors: list[Author]
    publishers: list[Publisher]
    publish_date: date | None = None
    author: str
    publisher: str

    @field_validator("source_records", "authors", "publishers")
    @classmethod
    def list_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("list must not be empty")
        return v
