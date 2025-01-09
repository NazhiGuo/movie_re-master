import pandas as pd
from sqlalchemy import create_engine, inspect


def import_movies(csv_path, db_path):
    # 读取 CSV 文件
    try:
        movies_df = pd.read_csv(csv_path)
        print("CSV 文件内容：")
        print(movies_df.head())  # 输出前几行以检查内容
    except FileNotFoundError:
        print(f"未找到 CSV 文件：{csv_path}")
        return
    except Exception as e:
        print(f"读取 CSV 文件时出错: {e}")
        return

    # 创建 SQLite 数据库引擎（如果不存在，将自动创建）
    engine = create_engine(f'sqlite:///{db_path}')

    # 将数据写入数据库中的 'movies' 表
    try:
        movies_df.to_sql('movies', engine, if_exists='replace', index=False)
        print(f"成功将 {csv_path} 导入到数据库 {db_path} 的 'movies' 表中。")
    except Exception as e:
        print(f"导入数据库时出错: {e}")
        return

    # 检查数据库中是否存在 'movies' 表，并打印内容
    try:
        inspector = inspect(engine)
        if 'movies' in inspector.get_table_names():
            print("'movies' 表已成功创建。")
            with engine.connect() as conn:
                result = conn.execute("SELECT * FROM movies LIMIT 5")
                rows = result.fetchall()
                print("数据库中的前几行数据：")
                for row in rows:
                    print(row)
        else:
            print("数据库中没有找到 'movies' 表。")
    except Exception as e:
        print(f"查询数据库时出错: {e}")


def collect_numbers_multiline():
    print("请输入多行文件名（例如 '12345.jpg'），输入 'y' 表示输入完成：")
    lines = []
    while True:
        line = input()
        if line.lower() == 'y':
            break
        lines.append(line)

    numbers = []
    for line in lines:
        filenames = line.split()
        for filename in filenames:
            if filename.endswith(".jpg"):
                number_part = filename.split(".")[0]
                numbers.append(int(number_part))

    print(numbers)
    return numbers


collect_numbers_multiline()

# csv_path = '../movies.csv'  # 替换为实际的 CSV 文件路径
# db_path = '../movies.db'  # SQLite 数据库文件名
#
#     # 导入数据到 SQLite 数据库
# import_movies(csv_path, db_path)
