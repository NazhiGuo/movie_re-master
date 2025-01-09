from flask import Flask, request, jsonify, render_template, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.Data_Set import Movie
import os
import sys

# 导入推荐函数
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
from utils.recommend import recommend_items

app = Flask(__name__)

# 配置数据库
DATABASE_PATH = './movies.db'  # 数据库文件路径
engine = create_engine(f'sqlite:///{DATABASE_PATH}', connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)

@app.before_request
def before_request():
    # 每个请求创建一个新的数据库 Session
    g.session = Session()

@app.teardown_request
def teardown_request(exception):
    # 每个请求结束后关闭数据库 Session
    session = g.get('session')
    if session:
        session.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    if not data or 'userId' not in data:
        return jsonify({'error': '缺少 userId 参数'}), 400

    user_id = data['userId']
    page = data.get('page', 1)
    page_size = 8

    start = (page - 1) * page_size
    end = start + page_size

    try:
        recommended_items = recommend_items(user_id)

        if not recommended_items:
            return jsonify({'message': '没有找到推荐的电影'}), 200

        recommended_page = recommended_items[start:end]

        if not recommended_page:
            return jsonify({'message': '没有更多推荐电影'}), 200

        recommended_movie_ids = [item[0] for item in recommended_page]

        # 使用 g.session 来查询数据库
        movies = g.session.query(Movie).filter(Movie.movieId.in_(recommended_movie_ids)).all()

        movie_dict = {movie.movieId: movie.title for movie in movies}
        recommendations = []
        for movie_id, score in recommended_page:
            title = movie_dict.get(movie_id, 'Unknown Title')
            recommendations.append({'movieId': movie_id, 'title': title, 'score': score})

        return jsonify({'recommendations': recommendations}), 200

    except Exception as e:
        print(f"推荐过程中出错: {e}")
        return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
