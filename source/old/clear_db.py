import sqlite3
import os

def get_parent_dir(directory):
    return os.path.dirname(directory)

parent = get_parent_dir(os.getcwd())
os.chdir("{0}/data".format(parent))

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

sql = """
DELETE FROM esp;
DELETE FROM sqlite_sequence where name='esp';
DELETE FROM opencv;
DELETE FROM sqlite_sequence where name='opencv';
"""

cursor.executescript(sql)
conn.commit()
conn.close()