
# -*- coding: utf-8 -*-
# DB 초기화 및 저장
import pymysql
import modeling

HOST = "127.0.0.1"
USER = "user"
PASSWD = "1004"

MOVIE_DBNAME = "movie"


def create_db(conn, cursor):
    sql = f"""CREATE DATABASE {MOVIE_DBNAME}"""
    drop = f"""DROP DATABASE IF EXISTS {MOVIE_DBNAME}"""
    cursor.execute(drop)
    cursor.execute(sql)
    conn.commit()


def connect():
    conn = pymysql.connect(host=HOST, user=USER,
                           password=PASSWD, port=13306, charset='utf8')
    cursor = conn.cursor()
    return conn, cursor


def create_table(conn, cursor):
    table_sql = f"""CREATE TABLE {MOVIE_DBNAME}.movie_info (\
        code_id INT NOT NULL PRIMARY KEY,\
        title VARCHAR(200),\
        actual_score FLOAT,\
        spc_score FLOAT,\
        net_score FLOAT,\
        genre VARCHAR(100),\
        country VARCHAR(100),\
        running_time VARCHAR(100),\
        director VARCHAR(100),\
        actors VARCHAR(200),\
        cnt INT\
            ) charset=utf8;"""
    drop = f"""DROP TABLE IF EXISTS {MOVIE_DBNAME}.movie_info"""
    cursor.execute(drop)
    cursor.execute(table_sql)
    conn.commit()


def arr_to_string(data):
    for item in data:

        try:
            item['genre'] = ",".join(item['genre'])
        except:
            item['genre'] = ""

        try:
            item['country'] = ",".join(item['country'])
        except:
            item['country'] = ""

        try:
            item['actors'] = ",".join(item['actors'])
        except:
            item['actors'] = ""
    return data


def insert_data(conn, cursor, data):
    insert_sql = f"""INSERT INTO {MOVIE_DBNAME}.movie_info (\
        code_id, title, actual_score, spc_score, net_score, genre, country, running_time, director, actors, cnt)\
        VALUES( %(code)s, %(title)s, %(actual_score)s, %(spc_score)s, %(net_score)s, %(genre)s, %(country)s, %(running_time)s, %(director)s, %(actors)s, %(count)s);\
    """

#    test_sql = f"""INSERT INTO {MOVIE_DBNAME}.movie_info (\
#        code_id, title, actual_score, spc_score, net_score, genre, country, running_time, director, actors, cnt )\
#        VALUES( %(code)s, %(title)s, %(actual_score)s, %(spc_score)s, %(net_score)s, %(genre)s, %(country)s, %(running_time)s, %(director)s, %(actors)s, %(count)s );\
#    """
#    temp = [{
#        "code": 1, "title": "test", "actual_score": 12.1, "spc_score": 4.5, "net_score": 2.2, "genre": ["멜로"], "country": ["한국", "미국"], "running_time": "120분", "director": "우치다", "actors": "우치다", "count": "112"
#    }, {
#        "code": 3, "title": "test", "actual_score": 12.3, "spc_score": 45, "net_score": 3.2, "genre": ["멜로"], "country": "한국", "running_time": "120분", "director": "우치다", "actors": "우치다,마토코", "count": "112"
#    }]

    # 변환

    data = arr_to_string(data)
    # cursor.execute(insert_sql, data)

    for item in data:
        # print(item)
        # print("\n")
        cursor.execute(insert_sql, item)
        conn.commit()


def read_data(conn, cursor):
    read_sql = f"""SELECT * FROM {MOVIE_DBNAME}.movie_info;"""

    cursor.execute(read_sql)
    return cursor.fetchall()



if __name__ == "__main__":
    conn, cursor = connect()
    create_db(conn, cursor)

    data = modeling.load_data()
    create_table(conn, cursor)
    insert_data(conn, cursor, data)
    print(read_data(conn, cursor))

    conn.commit()
    conn.close()