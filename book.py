"""
Book class for Library Inventory Manager
"""

from dataclasses import dataclass, asdict


@dataclass
class Book:
    """
    Represents a single book in the library.
    Attributes:
        title: Title of the book (str)
        author: Author name (str)
        isbn: Unique identifier for the book (str)
        status: "available" or "issued" (str)
    """
    title: str
    author: str
    isbn: str
    status: str = "available"

    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status}"

    def to_dict(self) -> dict:
        """Return a JSON-serializable dict representing the book."""
        return asdict(self)

    def issue(self) -> None:
        """Mark the book as issued if it is available."""
        if self.status == "issued":
            raise ValueError(f"Book '{self.title}' is already issued.")
        self.status = "issued"

    def return_book(self) -> None:
        """Mark the book as available."""
        if self.status == "available":
            raise ValueError(f"Book '{self.title}' is not issued.")
        self.status = "available"

    def is_available(self) -> bool:
        """Return True if the book is available."""
        return self.status == "available"
