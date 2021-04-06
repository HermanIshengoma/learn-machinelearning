#!/usr/bin/env python

# -----------------------------------------------------------------------
# database.py
# -----------------------------------------------------------------------

import os, json, pytz
import psycopg2
from config import config
import logging
from chapter import Chapter

DATABASE_URL = os.environ.get('DATABASE_URL')
CHAPTER_IDS = os.environ.get('CHAPTER_IDS').split(',')

#------------------------------------------------------------------------

class Database:

	def __init__(self, app=None):
		self._conn = None
		self._app = app

    # connect to the PostgreSQL server
	def connect(self):
		try:

			self._conn = psycopg2.connect(DATABASE_URL, sslmode='require')

		except (Exception, psycopg2.DatabaseError) as error:
			if self._app is not None:
				self._app.logger.warning(str(error))
			else:
				print(str(error))


    # close connection to the PostgreSQL server
	def disconnect(self):
		if self._conn is not None:
			self._conn.close()


    # add user if does not exist in database
	def user_exist(self, user_id):
		try:
			cur = self._conn.cursor()
		    # username = str(username)
			cmd = "SELECT user_id FROM public.\"users\" WHERE user_id = CAST((%s) as text)"
			cur.execute(cmd, (user_id, ))
			if cur.fetchone() is None:
				cmd2 = "INSERT INTO public.\"user\" (id, " + \
						"name)  " + \
						"VALUES (%s, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)"
				cur.execute(cmd2, (user_id, ))
				self._conn.commit()
				cur.close()
				return False

			cur.close()
			return True
		except (Exception, psycopg2.DatabaseError) as error:
			if self._app is not None:
				self._app.logger.warning(str(error))
			else:
				print(str(error))


    # update username in database
	def update_username(self, new_username, user_id):
		try:
			cur = self._conn.cursor()
			cmd = "UPDATE public.\"users\" " + \
					"SET name = CAST((%s) as text) " + \
					"WHERE id = CAST((%s) as text)"
			cur.execute(cmd, [new_username, user_id, ])

			self._conn.commit()

            # close the communication with the PostgreSQL database
			cur.close()

		except (Exception, psycopg2.DatabaseError) as error:
			self._app.logger.warning(str(error))


