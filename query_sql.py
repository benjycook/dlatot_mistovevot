# -*- coding: utf-8 -*-

import sqlite3


sqlite_db_file = 'dlatot_db.sqlite'

conn = sqlite3.connect(sqlite_db_file)
cur = conn.cursor()
pass