"""
Script: PyGconverter
Author: Gbenga Michael
Description: This script helps to convert the bible file I downloaded from
txt to csv to make it compatible with openlp.
"""

import os
import re
import csv
from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class Book:
    name: str
    chapters: int


BOOKS: list[Book] = [
    Book(*book_info)
    for book_info in [
        ["Genesisi", 50],
        ["Eksodu", 40],
        ["Lefitiku", 27],
        ["Numeri", 36],
        ["Deuteronomi", 34],
        ["Joṣua", 24],
        ["Onidajọ", 21],
        ["Rutu", 4],
        ["1 Samueli", 31],
        ["2 Samueli", 24],
        ["1 Ọba", 22],
        ["2 Ọba", 25],
        ["1 Kronika", 29],
        ["2 Kronika", 36],
        ["Esra", 10],
        ["Nehemiah", 13],
        ["Esteri", 10],
        ["Jobu", 42],
        ["Psalmu", 150],
        ["Owe", 31],
        ["Oniwasu", 12],
        ["Orin", 8],
        ["Isaiah", 66],
        ["Jeremiah", 52],
        ["Ẹkún", 5],
        ["Esekieli", 48],
        ["Danieli", 12],
        ["Hosea", 14],
        ["Joeli", 3],
        ["Amosi", 9],
        ["Obadiah", 1],
        ["Jona", 4],
        ["Mika", 7],
        ["Nahumu", 3],
        ["Habakuku", 3],
        ["Sefaniah", 3],
        ["Hagai", 2],
        ["Sekariah", 14],
        ["Malaki", 4],
        ["Matteu", 28],
        ["Marku", 16],
        ["Luku", 24],
        ["Johanu", 21],
        ["Iṣe", 28],
        ["Romu", 16],
        ["1 Korinti", 16],
        ["2 Korinti", 13],
        ["Galatia", 6],
        ["Efesu", 6],
        ["Filippi", 4],
        ["Kolosse", 4],
        ["1 Tessalonika", 5],
        ["2 Tessalonika", 3],
        ["1 Timotiu", 6],
        ["2 Timotiu", 4],
        ["Titu", 3],
        ["Filemoni", 1],
        ["Heberu", 13],
        ["Jakọbu", 5],
        ["1 Peteru", 5],
        ["2 Peteru", 3],
        ["1 Johanu", 5],
        ["2 Johanu", 1],
        ["3 Johanu", 1],
        ["Juda", 1],
        ["Ifihàn", 22],
    ]
]


class PyGConverter:
    def __init__(self):
        self.txt_file: Optional[str] = None

    def load_txt_file(self, file_name: str):
        """This method loads the file to be
        worked only if the format is '.txt'"""
        if not file_name.endswith(".txt"):
            logger.error("Invalid file format")
        try:
            with open(file_name, "r") as f:
                self.txt_file = f.read()  # TODO: not load all the file in memory
                logger.info(f"Opened {file_name}")
        except FileNotFoundError:
            logger.error(f"File with name {file_name} does not exist")

    def _strip_txt_to_chapter(self, chapter: str, next_chapter: str):
        content = self.txt_file
        next_chapter_query = rf"\W{next_chapter}"
        chapter_query = rf"\W{chapter}"
        chapter_result = re.search(chapter_query, content)
        next_chapter_result = re.search(next_chapter_query, content)
        if chapter_result and next_chapter_result:
            start_index = chapter_result.span()[1] + 1
            end_index = next_chapter_result.span()[0] - 1
            logger.info(end_index)
            chapter_content = content[start_index:end_index]
            with open(f"chapters/{chapter}.txt", "w") as f:
                f.write(chapter_content)
            logger.info(f"Written chapter {chapter}")
        else:
            if next_chapter_result is None:
                logger.error(f"Next chapter: {next_chapter} not found")
            if chapter_result is None:
                logger.error(f"Chapter: {chapter} not found")
            logger.error("Unable to strip to chapter")

    def _strip_txt_last_chapter(self, chapter: str):
        content = self.txt_file
        query = rf"\W{chapter}"
        search_result = re.search(query, content)
        if search_result:
            end_index = len(content)
            start_index = search_result.span()[1] + 1
            logger.info(end_index)
            chapter_content = content[start_index:end_index]
            with open(f"chapters/{chapter}.txt", "w") as f:
                f.write(chapter_content)
            logger.error(f"Written chapter {chapter}")
        else:
            logger.error("Unable to strip to chapter")

    def strip_txt_to_chapter(self, chapter: str, next_chapter: str):
        """Strips the ".txt" input file to
        chapters, all chapters are stored in
        the chapters folder

        this method uses re module to sort out the
        chapters so the next_chapter has to be the
        chapter after the chapter we are trying to strip"""
        try:
            os.mkdir("chapters")
        except FileExistsError:
            ...  # do nothing if it's a file exist error
        finally:
            self._strip_txt_to_chapter(chapter, next_chapter)

    @staticmethod
    def _count_verses(chapter: str) -> int:
        """returns the number of verses
        present in that chapter"""
        file_path = f"chapters/{chapter}.txt"
        chapter_content = None
        with open(file_path, "r+") as f:
            chapter_content = f.read()
        verses = 1
        query = rf"\W{verses}"
        find_verses = re.search(query, chapter_content)
        while find_verses is not None:
            verses += 1
            query = rf"\W{verses}"
            find_verses = re.search(query, chapter_content)
        return verses - 1

    def _read_chapter(self, chapter: str) -> str:
        """Helps to open generated chapters in
        the generated chapters folder"""
        file_path = f"chapters/{chapter}.txt"
        content = None
        with open(file_path, "r+") as f:
            content = f.read()
        return content

    def chapter_to_csv(
        self, csv_name: str, chapter_name: str, book_name: str, chapter_number: str
    ):
        """
        After the input file has been striped to chapters,
        this method helps to write the chapter to csv via the csv file
        name supplied. Note: if the csv file exits, it append the chapter
        to the csv
        This method if for the small logic
        necessary for writing the chapter to csv"""
        content = self._read_chapter(chapter_name)
        verses_count = self._count_verses(chapter_name)
        counter = 0
        csv_name = f"{csv_name}.csv"
        csv_file = open(csv_name, "a+")
        with open(f"{csv_name}.csv", "a+") as csv_file:
            with csv.writer(csv_file) as csv_writer:
                current_verse = 0
                next_verse = 1
            while counter < verses_count:
                current_verse += 1
                next_verse += 1
                counter += 1
                if current_verse == verses_count:
                    verse_query = rf"\W{current_verse}"
                    start_index = re.search(verse_query, content).span()[0]
                    end_index = len(content)
                    if start_index != -1:
                        new_verse = content[start_index:end_index]
                        new_row = [book_name, chapter_number, current_verse, new_verse]
                        csv_writer.writerow(new_row)
                else:
                    verse_query = rf"\W{current_verse}"
                    rv_query = rf"\W{next_verse}"
                    start_index = re.search(verse_query, content).span()[0]
                    end_index = re.search(rv_query, content).span()[0] - 1
                    if start_index != -1 and end_index != -1:
                        new_verse = content[start_index:end_index]
                        new_row = [book_name, chapter_number, current_verse, new_verse]
                        csv_writer.writerow(new_row)

    def _books_gen(self, books: list[Book]):
        """This function is a generator for
        books in the book_list"""
        for book in books:
            yield book

    def create_chapters(self, books: list[Book]):
        """This method creates the chapters
        for all the book of the input"""

        books = self._books_gen(books)
        next_book = next(books)

        for book in books:
            current_chapter = 1
            next_chapter = 2
            while current_chapter < book.chapters:
                self.strip_txt_to_chapter(
                    chapter=f"{book.name} {current_chapter}", next_chapter=f"{book.name} {next_chapter}"
                )
                current_chapter += 1
                next_chapter += 1
            if current_chapter == book.chapters:
                try:
                    next_book = next(books)
                    self.strip_txt_to_chapter(
                        chapter=f"{book.name} {current_chapter}", next_chapter=f"{next_book.name} 1"
                    )
                    current_chapter = 1
                    next_chapter = 2
                except StopIteration:
                    self._strip_txt_last_chapter(f"{book.name} {book.chapters}")
                    logger.info("All chapters completely written")

    def chapters_to_csv(self, csv_name: str, books: list[Book]):
        for book in books:
            max_count = book.chapters
            counter = 1
            logger.info(f"Converting {book.name} chapter {counter} to csv")
            while counter <= max_count:
                self.chapter_to_csv(
                    csv_name=csv_name,
                    chapter_name=f"{book.name} {counter}",
                    book_name=book.name,
                    chapter_number=str(counter),
                )
                logger.info(f"Added {book.name} chapter {counter} to {csv_name}")
                counter += 1
        logger.info(f"Completely added all books to {csv_name}")


if __name__ == "__main__":
    g = PyGConverter()
    g.load_txt_file("x.txt")
    g.create_chapters(BOOKS)
    g.chapters_to_csv("verses", BOOKS)
