import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
database_file = BASE_DIR / "data/weather.db"
sql_file = BASE_DIR / "sql/analysis.sql"


# Connect to SQLite database
with sqlite3.connect(database_file) as connection:
    queries = sql_file.read_text(encoding="utf-8")
    
    # Execute each query separately
    for query in queries.split(";"):
        if not query.strip():
            continue
        
        cursor = connection.execute(query)
        
        print("\nQuery result:")
        for row in cursor.fetchall():
            print(row)