# -*- coding: utf-8 -*-
import Scrapper
import pickle
import os


DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")


def download():

    # DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")

    # page 20개 (20*20)
    code_list = []
    for year in [2019, 2020, 2021]:
        for page in range(1, 21, 1):
            print(f"{year}, {page} 하는중입니다.")
            try:
                code_list.extend(Scrapper.get_movie_code(year, page))
            except:
                pass

    # print(code_list)

    move_info = {}
    count = 0
    for movie in code_list:
        for key, item in movie.items():
            count += 1
            print(f" {key}, {item} 하는중입니다. {count}")
            try:
                move_info[key] = Scrapper.get_movie_info(key, item)
            except:
                pass

    # print(len(move_info))

    # print(move_info)

    with open(DATA_PATH+'/movie_info.pkl', 'wb') as f:
        pickle.dump(move_info, f)


if __name__ == "__main__":
    download()
