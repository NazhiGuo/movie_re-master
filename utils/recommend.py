import pandas as pd
import numpy as np

# 加载用户因子
user_factors_df = pd.read_csv(r"F:\Dowloadn\movie_re-master\movie_recom-master\utils\user_factors.csv")  # 包含 'id' 和 'features' 列

# 加载物品因子
item_factors_df = pd.read_csv(r"F:\Dowloadn\movie_re-master\movie_recom-master\utils\item_factors.csv")  # 包含 'id' 和 'features' 列

import ast

# 将字符串转换为数值数组
user_factors_df['features'] = user_factors_df['features'].apply(ast.literal_eval).apply(np.array)
item_factors_df['features'] = item_factors_df['features'].apply(ast.literal_eval).apply(np.array)

user_factors = dict(zip(user_factors_df['id'], user_factors_df['features']))

# 创建物品因子字典
item_factors = dict(zip(item_factors_df['id'], item_factors_df['features']))

def predict_rating(user_id, item_id):
    '''
    根据用户 ID 和物品 ID，计算预测评分。
    '''
    user_vector = user_factors.get(user_id)
    item_vector = item_factors.get(item_id)
    if user_vector is not None and item_vector is not None:
        # 计算向量点积
        rating = np.dot(user_vector, item_vector)
        return rating
    else:
        return None


def recommend_items(user_id):
    '''
    为指定用户推荐前 N 个物品。
    '''
    user_vector = user_factors.get(user_id)
    if user_vector is None:
        print(f"User ID {user_id} not found.")
        return None

    # 计算所有物品的评分
    scores = []
    for item_id, item_vector in item_factors.items():
        rating = np.dot(user_vector, item_vector)
        scores.append((item_id, rating))

    # 按评分从高到低排序
    scores.sort(key=lambda x: x[1], reverse=True)

    # 返回前 N 个物品
    return scores
c=recommend_items(575)
print(c[:8])