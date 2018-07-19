import sqlite3
import os

def get_parent_dir(directory):
    return os.path.dirname(directory)

parent = get_parent_dir(os.getcwd())
os.chdir("{0}/data".format(parent))


conn = sqlite3.connect("data.db")
cursor = conn.cursor()

sql_delete = """
DELETE FROM esp;
DELETE FROM sqlite_sequence where name='esp';
DELETE FROM opencv;
DELETE FROM sqlite_sequence where name='opencv';
"""
cursor.executescript(sql_delete)
conn.commit()
conn.close()

os.remove('data.db')
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

sql_esp="""
CREATE TABLE esp(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
esp_num INTEGER NOT NULL,
time REAL NOT NULL,
ax REAL NOT NULL,
ay REAL NOT NULL,
az REAL NOT NULL,
gx REAL NOT NULL,
gy REAL NOT NULL,
gz REAL NOT NULL,
emg REAL NOT NULL);
"""

sql_opencv="""
CREATE TABLE opencv(
id INTEGER primary key AUTOINCREMENT,
x REAL NOT NULL,
y REAL NOT NULL);
"""

cursor.executescript(sql_esp)
cursor.executescript(sql_opencv)
conn.commit()
conn.close()
