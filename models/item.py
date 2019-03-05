import sqlite3


class Item:
    def __init__(self, _id, name, price):
        self.id = _id
        self.name = name
        self.price = price

    def json(self):
        return {'id': self.id, 'name': self.name, 'price': self.price}

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_item_query = 'INSERT INTO Items VALUES (NULL, ?, ?)'
        res = cursor.execute(insert_item_query, (self.name, self.price))
        self.id = res.lastrowid

        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE Items SET name=?, price=? WHERE id=?"
        cursor.execute(query, (self.id, self.name, self.price))

        connection.commit()
        connection.close()

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM Items WHERE id=?'
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(row[0], row[1], row[2])

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM Items WHERE name=?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            item = {'id': row[0], 'name': row[1], 'price': row[2]}
            return item
