import os
from funcutils import get_driver, get_env, read_list_pdf, write_pdf
from chapter import Chapter
from selenium.webdriver.common.by import By

class Manga:


    def extract_path(self, url: str, url_suffix: str, root_path: str) -> str:
        splited = url.split("/")
        index = len(splited) -1

        if not splited[-1]:
            index = index -1
        
        item = splited[index].lower().replace(url_suffix, "")
        return os.path.join(root_path, item)
    

    def extract_url_chapters(self):
        urls = []
        transform = lambda x: {"link": x.get_attribute("href"), "name": x.text}

        try:
            driver = get_driver()

            driver.get(self.url)
            urls = list(map(transform, driver.find_element(By.CLASS_NAME, get_env()["list_chapters"]).find_elements(By.TAG_NAME, "a")))

            print(f"+++ Chapters {self.manga_path} +++")
            [print(f"{chapter['name']} -> {chapter['link']}") for chapter in urls]
            print(f"------")

            driver.quit()
        except Exception as e:
            print(f"Ocurred a error on extracting url chapters {self.url}: {e}")
            urls = []
        
        return urls
    

    def build_chapters(self):
        urls = self.extract_url_chapters()
        chapters = []

        if len(urls) > 0:
            chapters = [Chapter(url=url["link"], chapter_name=url["name"], manga_path=self.manga_path) for url in urls]
        
        return chapters
    

    def mkdir(self):
        path = self.manga_path

        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created directory {path}")
    

    def build(self):
        self.mkdir()
        [chapter.save_chapter_content() for chapter in self.build_chapters()]
        self.build_compiled_chapters()
    

    def __convert_chapter_id(self, chapter_file_name: str) -> float:
        text = chapter_file_name.strip().lower().replace("chapter-", "").replace(".pdf", "").replace("_", ".")
        text = text[text.rfind("/")+1:]
        return float(text)
    

    def build_compiled_chapters(self):
        output_file_name = os.path.join(self.manga_path, "chapter-all.pdf")
        
        sorting_chapters = self.__convert_chapter_id
        chapters = sorted(read_list_pdf(self.manga_path), key=sorting_chapters)
        write_pdf(chapters, output_file_name)


    def __init__(self, url: str, url_suffix: str, root_path: str) -> None:
        self.url = url.strip().lower()
        self.url_suffix = url_suffix.strip().lower()
        self.root_path = root_path.strip()
        self.manga_path = self.extract_path(self.url, self.url_suffix, self.root_path)


    def __eq__(self, other: object) -> bool:
        return other and isinstance(other, Manga) and self.url == other.url
    

    def __str__(self) -> str:
        return f"url: {self.url}"
    

    def __hash__(self) -> int:
        return hash(self.url)
