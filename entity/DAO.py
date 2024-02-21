import mysql.connector

class DAO:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user='root',
            password='123456',
            database='quan_ly_model'
        )
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

