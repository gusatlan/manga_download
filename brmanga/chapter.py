from funcutils import get_driver, get_env
from page import Page
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select



class Chapter:


    def __extract_id(self, chapter_name: str) -> float:
        return float(chapter_name.strip().lower().replace("cap", "").replace("tulo", "").replace("í", "").replace("i", "").replace(" ", "").replace(",", ".").replace("v", "").replace("V", ""))


    def __extract_chapter_file_name(self, id: float) -> str:
        formatted = "{:06.1f}".format(id).replace(",", ".").replace(".", "_")

        return f"chapter-{formatted}.pdf"
    

    def __extract_chapter_path(self, manga_path: str) -> str:
        return os.path.join(manga_path)
    

    def __extract_chapter_path_file(self, manga_path: str, chapter_file_name: str) -> str:
        return os.path.join(manga_path, chapter_file_name)
    

    def __exists_chapter_path(self) -> bool:
        return os.path.exists(self.chapter_path)
    

    def __exists_chapter_file(self) -> bool:
        return os.path.exists(self.chapter_full_path)
    

    def mkdir(self):
        if not self.__exists_chapter_path():
            os.makedirs(self.chapter_path)
    

    def extract_url_pages(self):
        if not self.__exists_chapter_file():
            try:
                driver = get_driver()
                driver.get(self.url)

                Select(driver.find_element(By.ID, get_env()["element_read_mode"])).select_by_value(get_env()["select_read_mode"])
                urls = [str(image.get_attribute("src")) for image in driver.find_element(By.ID, get_env()["tag_image_all"]).find_elements(By.TAG_NAME, "img")]

                driver.quit()
                [print(f"Url for extract content {url}") for url in urls]
                return urls
            except Exception as e:
                print(f"Occured a error {e}")
                return []

        return []
    

    def build_pages(self):
        urls = self.extract_url_pages()
        return sorted([Page(url) for url in urls])
    

    def save_chapter_content(self):
        if not self.__exists_chapter_file():
            try:
                pages = self.build_pages()

                if pages:
                    self.mkdir()
                    imgs = [page.download() for page in pages]
                    imgs[0].save(self.chapter_full_path, save_all=True, append_images=imgs[1:])
                    print(f"Chapter builded {self.chapter_full_path}")
                    
            except Exception as e:
                print(f"Pages for {self.chapter_full_path} not loaded: {e}")
        else:
            print(f"Chapter already exists {self.chapter_full_path}")


    def __init__(self, url: str, chapter_name: str, manga_path: str) -> None:
        self.url = url
        self.chapter_name = chapter_name
        self.manga_path = manga_path
        self.id = self.__extract_id(self.chapter_name)
        self.chapter_file_name = self.__extract_chapter_file_name(self.id)
        self.chapter_path = self.__extract_chapter_path(self.manga_path)
        self.chapter_full_path = self.__extract_chapter_path_file(self.manga_path, self.chapter_file_name)
    

    def __str__(self) -> str:
        return f"{self.manga_path}{os.sep}{self.chapter_file_name}"
    

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Chapter) and self.chapter_file_name == other.chapter_file_name
    

    def __hash__(self) -> int:
        return hash(self.chapter_file_name)


    def __lt__(self, other) -> bool:
        return  self.id < other.id


    def __lte__(self, other) -> bool:
        return  self.id <= other.id


    def __gt__(self, other) -> bool:
        return  self.id > other.id


    def __gte__(self, other) -> bool:
        return  self.id >= other.id
