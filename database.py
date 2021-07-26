import sqlite3


class Database:

	def __init__(self, database):
		"""Connecting database file"""
		self.connection = sqlite3.connect(database)
		self.cursor = self.connection.cursor()

	def set_city(self, user_id, city):
		with self.connection:
			return self.cursor.execute("INSERT INTO cities_users (id, city) VALUES (?, ?)", (user_id, city))


	def user_exists(self, user_id):
		with self.connection:
			result = self.cursor.execute("SELECT * FROM cities_users WHERE id = ?", (user_id, )).fetchall()
			return bool(len(result))


	def update_city(self, user_id, city):
		with self.connection:
			return self.cursor.execute("UPDATE cities_users SET city = ? WHERE id = ?", (city, user_id))


	def get_city(self, user_id):
		with self.connection:
			result = self.cursor.execute("SELECT city FROM cities_users WHERE id = ?", (user_id, )).fetchall()
			return result[0][0]


	def close(self):
		self.connection.close()