import os
import shutil
import time
from exceptiongroup import catch
import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options


def __get_browser(url, element_name):
    browser = webdriver.Firefox()
    browser.get(url)

    elem = None
    if(element_name):
        elem = browser.find_element(By.CLASS_NAME, element_name)

    return browser, elem


def __get_env() -> tuple:
    """ Get env variables """
    
    list_path = os.getenv(key='DOWNLOAD_LIST_PATH',
                          default='/tmp/downloads/downloads.txt')
    download_path = os.getenv(key='DOWNLOAD_FOLDER', default='/tmp/downloads/')
    
    return list_path, download_path


def __mkdir(path: str, manga_title: str, chapter: str):
    """ Make directory and return path created """

    full_path = os.path.join(path, manga_title, chapter)
    os.makedirs(name=full_path, exist_ok=True)
    
    return full_path


def __read_download_manga_list(file_path: str):
    """ Read list of downloads """
    
    links = []
    with open(file_path) as file:
        for line in file:
            if(line):
                links.append(line)

    print("--- Download list ---")
    [print(f"Processing {link}") for link in links]
    print("----------------------")
    
    return links


def __split_manga_name_link(links):
    """ Split link in mangas name and link"""
    list_links = []

    for link in links:
        manga_name = list(filter(lambda x: x != "" and x != "\n" and x != "manga" and x != "https:" and x != "www.brmangas.net", link.split("/")))
        if(manga_name):
            list_links.append((manga_name[0].replace("-online", ""), link.replace("\n", "")))

    return list_links


def __get_chapter_url(url_manga_root, element_name):
    browser, elem = __get_browser(url_manga_root, element_name)

    chapters = [(
        "chapter-{:0>6}".format(
            float(
                el.find_element(By.TAG_NAME, "a")
                .text.lower()
                .replace("cap", "")
                .replace("tulo", "")
                .replace("í", "")
                .replace("i", "")
                .replace(" ", "")
                .replace(",", ".")
                .replace("v", "")
                .replace("V", "")
            )
        )
        .replace(".", "_")
        .replace("_0", ""),
        el.find_element(By.TAG_NAME, "a").get_attribute("href")) for el in elem.find_elements(By.TAG_NAME, "li")]

    browser.quit()
    return chapters


def __extract_full_path(root_path, links):
    """ Extract full path """
    download_list = []

    for manga in links:
        for chapter in manga[1]:
            path = __mkdir(
                path=root_path,
                manga_title=manga[0],
                chapter=chapter[0]
            )
            download_list.append((path, chapter[1]))
    
    return download_list


def __download_images(chapter):
    """ Download images and save to disk """
    save_to, link = chapter

    browser, _ = __get_browser(url=link, element_name=None)

    Select(browser.find_element(By.ID, "modo_leitura")).select_by_value("2")
    images = [str(image.get_attribute("src")) for image in browser.find_element(By.ID, "images_all").find_elements(By.TAG_NAME, "img")]

    for image in images:
        file = image.split("/")[-1]
        full_path_file = os.path.join(save_to, file)

        with open(full_path_file, "wb") as handler:
            handler.write(requests.get(image).content)
            print(f'Saved {full_path_file}')

    browser.quit()


def __convert_to_pdf(root_path, links_chapter):
    manga_dir = os.path.join(root_path, links_chapter[0][0])
    scan_dir = os.scandir(manga_dir)

    order = lambda x: float(x.split(os.sep)[-1].split(".")[0].replace("_", "."))

    for chapter in scan_dir:
        if chapter.is_dir and "chapter" in chapter.name:
            chapter_dir = os.scandir(chapter)
            filenames = []
            for file in chapter_dir:
                if file.is_file() and ("jpeg" in file.name.lower() or "jpg" in file.name.lower() or "png" in file.name.lower()):
                    filenames.append(file.path)

            filenames.sort(key=order)
            imgs = []

            for file in filenames:
                img = Image.open(file).convert("RGB")
                

                if "png" in file:
                    with BytesIO() as f:
                        img.save(f, format="JPEG")
                        f.seek(0)
                        img = Image.open(f).convert("RGB")

                imgs.append(img)

            chapter_file_name = f"{chapter.path}.pdf"
            try:
                imgs[0].save(chapter_file_name, save_all=True, append_images=imgs[1:])
                print(f"Chapter converted to PDF {chapter_file_name}")
                shutil.rmtree(chapter.path)
            except Exception as e:
                print(e)


def process():
    list_path, download_path = __get_env()
    links_root_mangas = __split_manga_name_link(__read_download_manga_list(list_path))

    links_chapters = [(link[0], __get_chapter_url(link[1], "capitulos")) for link in links_root_mangas]
    download_list = __extract_full_path(root_path=download_path, links=links_chapters)

    [__download_images(item) for item in download_list]
    __convert_to_pdf(download_path, links_chapters)
