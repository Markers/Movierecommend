from re import I
import requests
import sys
from bs4 import BeautifulSoup
import time

# 연도별
# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={year}&page=10000


def get_movie_code(year, page=1):
    movie_code_list = []

    year_url = f"https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={year}&page={page}"

    response = requests.get(year_url)
    time.sleep(1)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        direct_list = soup.find(class_="directory_list")
        ankers = direct_list.find_all("a", class_=False)

        for anker in ankers:
            code = anker['href'].split("=")[1]
            title = anker.text
            # print(code, title)
            movie_code_list.append({code: title})
    else:
        print(
            f"get_moive_code function -> status_code : {response.status_code} ")

    return movie_code_list


def change_point_to_score(point):
    score = ""
    try:
        for item in point:
            score += item.text
    except:
        score = 0

    return float(score)


def replace_data(data):
    return data.replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "").split(",")


def get_movie_info(code, title):
    movie_info_url = f"https://movie.naver.com/movie/bi/mi/basic.naver?code={code}"

    response = requests.get(movie_info_url)
    time.sleep(1)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        mv_info = soup.find(class_="mv_info")

        # title = mv_info.find(class_="h_movie").text
        # print(title)

        # score = mv_info.find_all(class_="score")

        try:
            # actualPoint 관람객 평점
            actual_point = soup.select_one(
                "#actualPointPersentBasic").select("em")
            actual_score = change_point_to_score(actual_point)
        # print(actual_score)
        except:
            actual_score = 0.0

        try:
            # spc_score 평론가 평점
            spc_point = soup.select_one(".spc").select_one(
                ".star_score").select("em")
            spc_score = change_point_to_score(spc_point)
        # print(spc_score)
        except:
            spc_score = 0.0

        try:
            # pointNetizenPersentBasic 네티즌 평점
            net_point = soup.select_one(
                "#pointNetizenPersentBasic").select("em")
            net_score = change_point_to_score(net_point)
        # print(net_score)
        except:
            net_point = 0.0

        # info spec
        info_spec_span = soup.select(".info_spec")[1].select("span")
        info_spec = soup.select(".info_spec")[1]

        try:
            # genre 장르
            # .replace(" ","").replace("\n","").replace("\t","").replace("\r","").split(",")
            genre = info_spec_span[0].get_text()
            genre = replace_data(genre)
        # print(replace_data(genre))
        except:
            genre = None

        try:
            # 나라
            country = info_spec_span[1].get_text()
            country = replace_data(country)
        # print(replace_data(country))
        except:
            country = None

        try:
            # 영화 시간
            running_time = info_spec_span[2].get_text()
        # print(running_time)
        except:
            ruunnig_time = 0

        try:
            # director 감독
            director = info_spec.select_one(
                ".step2").next_sibling.next_sibling.get_text()
        except:
            director = None

        try:
            # actor 배우
            actors = info_spec.select_one(
                ".step3").next_sibling.next_sibling.get_text().replace("더보기", "")
            actors = replace_data(actors)
        # print(actors)
        except:
            actors = None

        try:
            # count 누적관객
            # 표시 안되는 경우도 있음.
            count = info_spec.select_one(".count").get_text().split("명")[
                0].replace(",", "")
            count = int(count)
            # print(count)
        except:
            count = 0
            # print(count)

    return {
        "title": title,
        "actual_score": actual_score,
        "spc_score": spc_score,
        "net_score": net_score,
        "genre": genre,
        "country": country,
        "running_time": running_time,
        "director": director,
        "actors": actors,
        "count": count,
        "code": code
    }


if __name__ == "__main__":
    argument = sys.argv
    if len(argument) != 2:
        print(f"연도를 입력해주세요.:")
    else:
        del argument[0]  # 파일이름 지운다.
        print(f"입력한 연도는 {argument[0]} 입니다")
        code_list = get_movie_code(argument[0])

        for movie in code_list:
            for key, item in movie.items():
                # print(key, item)
                print(get_movie_info(key, item))
            # print(movie.items())
            # print(movie)
        # print(code_list)
        # print(get_movie_info(57095))
        # print(get_movie_info(208655))
