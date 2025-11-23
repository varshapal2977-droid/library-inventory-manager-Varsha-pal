"""
LibraryInventory: manages a collection of Book objects with JSON persistence.
"""
import json
import logging
from pathlib import Path
from typing import List, Optional

from library_manager.book import Book

logger = logging.getLogger(__name__)


class LibraryInventory:
    def __init__(self, storage_path: Path):
        """
        storage_path: Path to JSON file for persistence.
        """
        self.storage_path = storage_path
        self.books: List[Book] = []
        self._ensure_storage_dir_exists()
        self.load_from_file()

    def _ensure_storage_dir_exists(self):
        if not self.storage_path.parent.exists():
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def add_book(self, book: Book) -> None:
        """Add a book object to inventory; raise if ISBN already exists."""
        if self.search_by_isbn(book.isbn) is not None:
            logger.error("Attempt to add duplicate ISBN: %s", book.isbn)
            raise ValueError(f"A book with ISBN {book.isbn} already exists.")
        self.books.append(book)
        logger.info("Added book: %s", book)
        self.save_to_file()

    def search_by_title(self, title: str) -> List[Book]:
        """Return list of books whose titles contain the case-insensitive title fragment."""
        title_lower = title.strip().lower()
        return [b for b in self.books if title_lower in b.title.lower()]

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        """Return a Book by ISBN or None if not found."""
        for b in self.books:
            if b.isbn.strip() == isbn.strip():
                return b
        return None

    def display_all(self) -> List[Book]:
        """Return all books as a list."""
        return list(self.books)

    def issue_book(self, isbn: str) -> None:
        """Issue a book by ISBN (change status)."""
        book = self.search_by_isbn(isbn)
        if book is None:
            logger.error("Attempt to issue non-existent book ISBN: %s", isbn)
            raise LookupError(f"No book found with ISBN {isbn}")
        book.issue()
        logger.info("Book issued: %s", book)
        self.save_to_file()

    def return_book(self, isbn: str) -> None:
        """Return a book by ISBN (change status)."""
        book = self.search_by_isbn(isbn)
        if book is None:
            logger.error("Attempt to return non-existent book ISBN: %s", isbn)
            raise LookupError(f"No book found with ISBN {isbn}")
        book.return_book()
        logger.info("Book returned: %s", book)
        self.save_to_file()

    def save_to_file(self) -> None:
        """Persist current inventory to JSON file with safe write and logging."""
        try:
            data = [b.to_dict() for b in self.books]
            tmp_path = self.storage_path.with_suffix(".tmp")
            with tmp_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            tmp_path.replace(self.storage_path)
            logger.info("Successfully saved %d books to %s", len(self.books), self.storage_path)
        except Exception as ex:
            logger.exception("Failed to save inventory to %s: %s", self.storage_path, ex)
            raise

    def load_from_file(self) -> None:
        """Load inventory from JSON file. Gracefully handle missing or corrupted file."""
        if not self.storage_path.exists():
            # No file yet; create empty list and save a fresh JSON file
            self.books = []
            try:
                self.save_to_file()
            except Exception:
                # If save fails, log but continue with empty in-memory inventory
                logger.exception("Could not create initial storage file at %s", self.storage_path)
            return

        try:
            with self.storage_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            loaded = []
            for item in data:
                # Validate minimal structure
                if not all(k in item for k in ("title", "author", "isbn", "status")):
                    logger.warning("Skipping malformed entry in data file: %s", item)
                    continue
                loaded.append(Book(
                    title=str(item["title"]),
                    author=str(item["author"]),
                    isbn=str(item["isbn"]),
                    status=str(item.get("status", "available"))
                ))
            self.books = loaded
            logger.info("Loaded %d books from %s", len(self.books), self.storage_path)
        except json.JSONDecodeError:
            logger.exception("JSON decoding failed for file %s. Starting with empty inventory.", self.storage_path)
            self.books = []
        except Exception as ex:
            logger.exception("Unexpected error loading inventory: %s", ex)
            self.books = []
