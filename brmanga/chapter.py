from brmanga.funcutils import get_driver
import os


class Chapter:


    def __extract_chapter_file_name(self, chapter_name: str) -> str:
        number = float(chapter_name.strip().lower().replace("cap", "").replace("tulo", "").replace("í", "").replace("i", "").replace(" ", "").replace(",", ".").replace("v", "").replace("V", ""))
        formatted = "{:06.1f}".format(number).replace(",", ".").replace(".", "_")

        return f"chapter-{formatted}.pdf"


    def __init__(self, url: str, chapter_name: str, manga_path: str) -> None:
        self.url = url
        self.chapter_name = chapter_name
        self.manga_path = manga_path
        self.chapter_file_name = self.__extract_chapter_file_name(self.chapter_name)
    

    def __str__(self) -> str:
        return f"{self.manga_path}{os.sep}{self.chapter_file_name}"