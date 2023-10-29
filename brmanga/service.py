from funcutils import read_download_manga_list, get_env
from manga import Manga

def retrieve_mangas():
    urls = read_download_manga_list()
    envs = get_env()
    url_suffix = envs["url_suffix"]
    root_path = envs["download_path"]

    mangas = [Manga(url = url, url_suffix = url_suffix, root_path = root_path) for url in urls]
    return mangas


def build_mangas(mangas):
    [manga.build() for manga in mangas]
