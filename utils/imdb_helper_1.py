import imdb


def get_movie_info(title):
    """
    使用 IMDbPY 获取电影信息。

    :param title: 电影标题
    :return: 电影信息字典或 None
    """
    ia = imdb.IMDb(proxy="socks5://127.0.0.1:10808")
    try:
        # 搜索电影
        search_results = ia.search_movie(title)
        if not search_results:
            print(f"未找到电影: {title}")
            return None

        # 获取第一个搜索结果的详细信息
        movie = search_results[0]
        ia.update(movie)

        # 提取所需信息
        movie_info = {
            'title': movie.get('title'),
            'year': movie.get('year'),
            'rating' :movie.get('rating'),
            'directors': [d['name'] for d in movie.get('directors', [])],
            'cast': [cast['name'] for cast in movie.get('cast', [])][:5],
            'img_url': movie.get('full-size cover url')
        }

        return movie_info
    except Exception as e:
        print(f"获取电影信息时出错: {e}")
        return None
get_movie_info("Pulp Fiction (1994)")