import sqlite3
import pandas as pd

class DBManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

    def get_objects(self, obj_type):
        query = f"SELECT name FROM sqlite_master WHERE type='{obj_type}';"
        return pd.read_sql_query(query, self.conn)['name'].tolist()

    def run_script(self, script):
        """복합 SQL 스크립트 실행"""
        try:
            clean_script = script.replace('\xa0', ' ').strip()
            self.conn.executescript(clean_script)
            self.conn.commit()
            return True, "성공"
        except Exception as e:
            return False, str(e)

    def fetch_dataframe(self, table_name, limit=1000):
        query = f'SELECT * FROM "{table_name}" LIMIT {limit}'
        return pd.read_sql_query(query, self.conn)

    def close(self):
        self.conn.close()
