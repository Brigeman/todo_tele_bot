import sqlite3

# создаем подключение к базе данных
conn = sqlite3.connect('my.db')

# создаем таблицу task в базе данных
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS task (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        done INTEGER
    )
''')
conn.commit()

# закрываем подключение к базе данных
# conn.close()

