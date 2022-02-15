# -*- coding: utf-8 -*-
import pickle
import os
from re import I
import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")
# 네이버 영화 장르 정보
# 드라마, 판타지, 서부, 공포, 멜로/로맨스, 모험, 스릴러, 느와르, 컬트, 다큐멘터리, 코미디, 가족, 미스터리, 전쟁, 애니메이션, 범죄, 뮤지컬, SF,액션, 무협, 에로, 서스펜스, 서사, 블랙코미디, 실험, 공연실황

GERNE = ["드라마", "판타지", "서부", "공포", "멜로/로맨스", "모험", "스릴러", "느와르", "컬트", "다큐멘터리", "코미디", "가족",
         "미스터리", "전쟁", "애니메이션", "범죄", "뮤지컬", "SF", "액션", "무협", "에로", "서스펜스", "서사", "블랙코미디", "실험", "공연실황"]

gerne_number = [x for x in range(0, 26)]

gerne_id = dict(zip(GERNE, gerne_number))


def load_data():
    with open(DATA_PATH+'/movie_info.pkl', 'rb') as f:
        data = pickle.load(f)

    # print(data)

    return list(data.values())


def matrix(data):
    result = []
    for i in data:
        inner_list = []
        for v in i:
            if v in gerne_id.keys():
                inner_list.append(gerne_id[v])
        result.append(inner_list)

    return result


def save_matrix(data, code_list):

    df_concat = pd.concat([code_list, data], axis=1)
    matrix = df_concat.values.tolist()
    # print(matrix)

    with open(DATA_PATH+'/matrix_data.pkl', 'wb') as f:
        pickle.dump(matrix, f)

    # test = pd.DataFrame([[1,23,3,45,1],[1,23,3,45,1],[1,23,3,45,1]])
    # print(test.values.tolist())


def recommend(code):

    data = load_data()
    df = pd.DataFrame(data)
    result = matrix(df.genre)
    # print(result)

    score = np.zeros((len(df), 26))  # 100 x 26  0으로 채움
    # print(score.shape)

    for i, v in enumerate(result):
        for w in v:
            score[i, w] = 1.0

    # print(score)

    cosine_similar = cosine_similarity(score, score)

    # 자기 자신에 대한 유사도 제외
    for i in range(len(df)):
        cosine_similar[i, i] = 1.0

    cosine_similar_data = pd.DataFrame(cosine_similar)
    # print(cosine_similar_data.head(10))
    # print(cosine_similar.shape)
    save_matrix(cosine_similar_data, df.code)

    # 특정 영화에 관해서 찾기
    code = str(code)
    idx = df.loc[df.code == code].index.item()
    # print("idx : ", idx)

    sim_scores = list(enumerate(cosine_similar_data[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # print(sim_scores[1:10])

    movie_indices = [i[0] for i in sim_scores]

    choice = []
    for i in range(10):
        choice.append(df['title'][movie_indices[i]])
        # 가장 유사한 10개의 영화의 제목을 리턴합니다.

    # print('***영화 추천 순위***')
    # for i in range(10):
        # print(str(i+1) + '순위 : ' + choice[i])


# recommend(189051)
recommend(187979)
# 189051
# 0번 index 177371
# 187979
