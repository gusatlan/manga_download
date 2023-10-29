import requests
from PIL import Image
from io import BytesIO

class Page:

    def __extract_name(self):
        return self.url[self.url.rfind("/")+1:].strip()


    def __extract_id(self):
        return float(self.name[:self.name.rfind(".")].strip().replace(",", ".").replace("_", "."))
    

    def __is_jpg(self) -> bool:
        return ".jpg" in self.name.lower() or ".jpeg" in self.name.lower()
    

    def download(self, retries: int = 5) -> Image.Image:
        image = None

        try:
            with BytesIO(requests.get(self.url).content) as f:
                image = Image.open(f).convert("RGB")
            
            print(f"Retrieved page image in raw {self.url}")

            if not self.__is_jpg():
                with BytesIO() as f:
                    image.save(f, format="JPEG")
                    f.seek(0)
                    image = Image.open(f).convert("RGB")
                
                print(f"Converted raw image to JPEG {self.name}")
        except Exception as e:
            if retries > 0:
                image = self.download(retries-1)
            print(f"Exception on download page: {e}")
            image = None

        return image


    def __init__(self, url:str):
        self.url = url
        self.name = self.__extract_name()
        self.id = self.__extract_id()


    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Page):
            return obj.url == self.url
        return False


    def __hash__(self) -> int:
        return hash(self.url)


    def __lt__(self, other) -> bool:
        return  self.id < other.id


    def __lte__(self, other) -> bool:
        return  self.id <= other.id

    
    def __gt__(self, other) -> bool:
        return  self.id > other.id


    def __gte__(self, other) -> bool:
        return  self.id >= other.id


    def __str__(self) -> str:
        return f'url: {self.url}, name: {self.name}, id: {self.id}'
