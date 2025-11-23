"""
Simple unit tests for LibraryInventory (uses built-in unittest)
Run: python -m pytest tests
"""
import tempfile
import json
from pathlib import Path

from library_manager.book import Book
from library_manager.inventory import LibraryInventory


def test_add_and_search_and_persistence(tmp_path: Path):
    storage = tmp_path / "books.json"
    inv = LibraryInventory(storage)

    b1 = Book(title="A", author="Author A", isbn="ISBN-A")
    b2 = Book(title="B", author="Author B", isbn="ISBN-B")

    inv.add_book(b1)
    inv.add_book(b2)

    # search by title
    assert len(inv.search_by_title("A")) == 1
    assert inv.search_by_isbn("ISBN-B").title == "B"

    # issue and return
    inv.issue_book("ISBN-A")
    assert inv.search_by_isbn("ISBN-A").status == "issued"
    inv.return_book("ISBN-A")
    assert inv.search_by_isbn("ISBN-A").status == "available"

    # check file was written
    with storage.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert any(item["isbn"] == "ISBN-A" for item in data)
