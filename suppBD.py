import sqlite3

db = sqlite3.connect('support_base.db')

cur = db.cursor()
cur.execute('''
CREATE TABLE supports (
id INTEGER PRIMARY KEY,
tgname TEXT NOT NULL,
number INTEGER NOT NULL,
text_supp TEXT NOT NULL
)''')


db.commit()
db.close()