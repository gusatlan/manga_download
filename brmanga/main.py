from service import retrieve_mangas, build_mangas


if __name__ == '__main__':
    mangas = retrieve_mangas()
    build_mangas(mangas)
