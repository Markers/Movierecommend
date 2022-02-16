from flask import Flask, render_template, request
from src import manage
from src import Scrapper, modeling
from numpy.random import choice

app = Flask(__name__)


@app.route('/')
def index():
    conn, cursor = manage.connect()
    data = manage.read_data(conn, cursor)

    choisen = choice(len(data), 9)

    random_movie_list = []
    for idx in choisen:
        poster_list = [Scrapper.get_poster(data[idx][0])]
        poster_data = list(data[idx]) + poster_list
        random_movie_list.append(poster_data)

    return render_template('index.html', data=random_movie_list)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    post_value = request.form['predict']
    result = modeling.recommend(post_value)
    return str(result), 200


@app.route('/recommend', methods=['POST'])
def recommend():
    post_value = request.form['predict']
    # print(post_value)
    choice_poster = Scrapper.get_poster(post_value)
    choice_info = Scrapper.get_movie_info(post_value)
    result = modeling.recommend(post_value)

#
    result_list = []
    for item in result:
        poster_list = [Scrapper.get_poster(item[10])]
        post_data = list(item) + poster_list
        result_list.append(post_data)
#
    # print(result[0])

    return render_template('result.html', data=result_list, poster_url=choice_poster, info=choice_info)


# @app.route('/predict', methods=['POST'])
# def home():
#     data1 = request.form['a']
#     data2 = request.form['b']
#     data3 = request.form['c']
#     data4 = request.form['d']
#     arr = np.array([[data1, data2, data3, data4]])
#     pred = model.predict(arr)
#     return render_template('after.html', data=pred)


if __name__ == "__main__":
    app.run(debug=True)
