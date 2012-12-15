#!/usr/bin/env python
#
#	Simplifying SQLite access
#
#	2012-12-14	Created by Pascal Pfiffner
#


import sqlite3


class _SQLite (object):
	""" SQLite access
	"""
	
	def __init__(self):
		self.handle = None
		self.cursor = None


	def execute(self, sql, params=()):
		""" Executes an SQL command and returns the cursor.execute, which can
		be used as an iterator.
		Supply the params as tuple, i.e. (param,) and (param1,param2,...)
		"""
		if not sql or len(sql) < 1:
			raise Exception('no SQL to execute')
		if not self.cursor:
			self.connect()
		
		return self.cursor.execute(sql, params)


	def executeOne(self, sql, params):
		""" Returns the first row returned by executing the command
		"""
		self.execute(sql, params)
		return self.cursor.fetchone()


	def create(self, table_name, table_structure):
		""" Executes a CREATE TABLE IF NOT EXISTS query with the given structure.
		Input is NOT sanitized, watch it!
		"""
		create_query = 'CREATE TABLE IF NOT EXISTS %s %s' % (table_name, table_structure)
		self.execute(create_query)


	def commit(self):
		self.handle.commit()


	def connect(self):
		if self.cursor is not None:
			return
		self.handle = sqlite3.connect('storage.db')
		self.cursor = self.handle.cursor()


	def close(self):
		if self.cursor is None:
			return
		self.handle.close()
		self.cursor = None
		self.handle = None


# singleton init whack-a-hack
SQLite = _SQLite()
del _SQLite