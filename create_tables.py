import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_user_table_sql = 'CREATE TABLE IF NOT EXISTS Users (id integer PRIMARY KEY, username text, password text)'
cursor.execute(create_user_table_sql)

create_item_table_sql = 'CREATE TABLE IF NOT EXISTS Items (id integer PRIMARY KEY, name text, price real)'
cursor.execute(create_item_table_sql)
# cursor.execute('INSERT INTO Items VALUES (NULL, "test", 10.99)')

connection.commit()
connection.close()
