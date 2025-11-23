"""
Command-line interface for Library Inventory Manager.
Run this file directly: python cli/main.py
"""

import logging
from pathlib import Path
import sys

from library_manager.book import Book
from library_manager.inventory import LibraryInventory


# Setup logging
LOG_FILE = Path("data") / "library.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("cli")

DATA_FILE = Path("data") / "books.json"


def prompt_menu() -> None:
    print("\n=== Library Inventory Manager ===")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search by Title")
    print("6. Search by ISBN")
    print("7. Exit")


def input_nonempty(prompt_text: str) -> str:
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def add_book_flow(inv: LibraryInventory) -> None:
    print("\n-- Add Book --")
    title = input_nonempty("Title: ")
    author = input_nonempty("Author: ")
    isbn = input_nonempty("ISBN: ")
    book = Book(title=title, author=author, isbn=isbn)
    try:
        inv.add_book(book)
        print(f"Book added: {book}")
    except ValueError as ex:
        print(f"Error: {ex}")


def issue_book_flow(inv: LibraryInventory) -> None:
    print("\n-- Issue Book --")
    isbn = input_nonempty("ISBN to issue: ")
    try:
        inv.issue_book(isbn)
        print("Book issued.")
    except LookupError as ex:
        print(f"Error: {ex}")
    except ValueError as ex:
        print(f"Error: {ex}")


def return_book_flow(inv: LibraryInventory) -> None:
    print("\n-- Return Book --")
    isbn = input_nonempty("ISBN to return: ")
    try:
        inv.return_book(isbn)
        print("Book returned.")
    except LookupError as ex:
        print(f"Error: {ex}")
    except ValueError as ex:
        print(f"Error: {ex}")


def view_all_flow(inv: LibraryInventory) -> None:
    print("\n-- All Books --")
    books = inv.display_all()
    if not books:
        print("No books in inventory.")
        return
    for i, b in enumerate(books, start=1):
        print(f"{i}. {b}")


def search_title_flow(inv: LibraryInventory) -> None:
    print("\n-- Search by Title --")
    q = input_nonempty("Enter title or part of title: ")
    found = inv.search_by_title(q)
    if not found:
        print("No books found.")
        return
    for b in found:
        print(b)


def search_isbn_flow(inv: LibraryInventory) -> None:
    print("\n-- Search by ISBN --")
    isbn = input_nonempty("ISBN: ")
    book = inv.search_by_isbn(isbn)
    if book is None:
        print("No book found.")
    else:
        print(book)


def main():
    inv = LibraryInventory(DATA_FILE)
    while True:
        try:
            prompt_menu()
            choice = input("Choose an option (1-7): ").strip()
            if choice == "1":
                add_book_flow(inv)
            elif choice == "2":
                issue_book_flow(inv)
            elif choice == "3":
                return_book_flow(inv)
            elif choice == "4":
                view_all_flow(inv)
            elif choice == "5":
                search_title_flow(inv)
            elif choice == "6":
                search_isbn_flow(inv)
            elif choice == "7":
                print("Exiting. Goodbye!")
                break
            else:
                print("Invalid option. Please choose a number between 1 and 7.")
        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting.")
            break
        except Exception as e:
            logger.exception("An unexpected error occurred: %s", e)
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
