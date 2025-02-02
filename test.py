import sqlite3


connection = sqlite3.connect('USERSDB.db')
cursor = connection.cursor()

# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS UsersDATA (
username TEXT NOT NULL,
email TEXT NOT NULL,
password TEXT PRIMARY KEY NOT NULL

)
''')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()