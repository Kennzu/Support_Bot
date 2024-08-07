import sqlite3

db = sqlite3.connect('support_base_m2.db')

cur = db.cursor()
cur.execute('''
CREATE TABLE supports (
id INTEGER PRIMARY KEY,
idnp TEXT NOT NULL,
tgname TEXT NOT NULL,
number INTEGER NOT NULL,
text_supp TEXT NOT NULL,
queue INTEGER NOT NULL,
status DEFAULT решается🛠
)''')

cur.execute('''
CREATE TABLE files (
id INTEGER PRIMARY KEY,
file_id TEXT NOT NULL,
hash_file_id TEXT NOT NULL,
file_name TEXT NOT NULL,
file BLOB )''')
# cur.execute('''SELECT queue from supports ORDER BY ROWID DESC LIMIT 1''')
# queue = cur.fetchone()
# print(queue)
# tr = " ".join(map(str, queue))
# print(tr)
# a = int(tr)+1
# print(a)

# cur.execute(f'''SELECT tgname, number, text_supp, queue from supports WHERE idnp == {callback.from_user.id}''')
# state_sup = cur.fetchall()
# print(state_sup)

# cur.execute("""SELECT * from supports""")
# a = cur.fetchall()
# for i in a:
#     print(i)



db.commit()
db.close()