import os
from selenium import webdriver
from PyPDF2 import PdfReader, PdfWriter


def get_driver(url: str = ""):
    browser = webdriver.Firefox()

    if url:
        browser.get(url)
    return browser


def get_env() -> dict:
    
    list_path = os.getenv(key='DOWNLOAD_LIST_PATH',
                          default='/media/dockstation/data/mangas/downloads.txt')
    download_path = os.getenv(key='DOWNLOAD_FOLDER', default='/media/dockstation/data/mangas')
    url_suffix = os.getenv(key='URL_SUFFIX', default='-online')
    list_chapters = os.getenv(key='LIST_CHAPTERS', default='capitulos')
    read_mode = os.getenv(key='READ_MODE', default='modo_leitura')
    select_read_mode = os.getenv(key='SELECT_READ_MODE', default='2')
    tag_image_all = os.getenv(key='IMAGE_ALL', default='images_all')
    
    
    
    return {
        "download_list": list_path,
        "download_path": download_path,
        "url_suffix": url_suffix,
        "list_chapters": list_chapters,
        "element_read_mode": read_mode,
        "select_read_mode": select_read_mode,
        "tag_image_all": tag_image_all
    }


def read_download_manga_list():
    file_path = get_env()["download_list"]
    
    links = []
    with open(file_path) as file:
        for line in file:
            if(line):
                links.append(line)

    print("--- Download list ---")
    [print(link) for link in links]
    print("----------------------")
    
    return links


def read_list_pdf(path: str = "./"):
    pdfs = []
    with os.scandir(path) as directory:
        for file in directory:
            if ".pdf" in file.name.lower().strip() and "all" not in file.name.lower():
                pdfs.append(file.path)
    return sorted(pdfs)


def write_pdf(pdfs: list, output_file_name: str):
    try:
        pdf_writer = PdfWriter()

        for pdf in pdfs:
            pdf_reader = PdfReader(pdf)
            num_pages = len(pdf_reader.pages)

            for page_index in range(num_pages):
                print(f"Adding page {page_index}/{num_pages}")
                page = pdf_reader.pages[page_index]
                pdf_writer.add_page(page)
        
        with open(output_file_name, "wb") as out:
            pdf_writer.write(out)
        print(f"Saved {output_file_name}")
    except Exception as e:
        print(f"Ocurred a error in save compiled chapters {output_file_name}: {e}")
