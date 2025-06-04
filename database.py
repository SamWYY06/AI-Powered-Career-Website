import mysql.connector # type: ignore

def get_connection():
    return mysql.connector.connect(
        host='localhost',  # or your MySQL host IP or domain
        user='root',
        password='',
        database='career_path',
        charset='utf8'  # Change charset to utf8 if utf8mb4 causes issues
    )
