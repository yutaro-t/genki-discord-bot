
from dotenv import load_dotenv
from os.path import join, dirname
load_dotenv(join(dirname(__file__),'../', '.env'))

import sqlite3
import os

DB_NAME = os.getenv('SQLITE3_DB_NAME')

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS account;")
cur.execute('''
CREATE TABLE account(
  discord_id STRING PRIMARY KEY,
  score INT,
  lol_id STRING
)
''')
cur.close()