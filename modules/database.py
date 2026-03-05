import sqlite3
import pandas as pd

class DBManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def run_script(self, script):
        """VIEW 생성 등 SQL 실행"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        try:
            # 특수 공백 제거
            clean_sql = script.replace('\xa0', ' ').strip()
            conn.executescript(clean_sql)
            conn.commit()
            return True, "성공"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    def get_objects(self, obj_type):
        """Table/View 목록 가져오기"""
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT name FROM sqlite_master WHERE type='{obj_type}';"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df['name'].tolist()

    def fetch_data(self, obj_name):
        """데이터 조회"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query(f'SELECT * FROM "{obj_name}" LIMIT 1000', conn)
        conn.close()
        return df
