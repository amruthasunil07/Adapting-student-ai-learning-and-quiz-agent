import sqlite3

conn = sqlite3.connect("app.db")
c = conn.cursor()

subj_cols = [r[1] for r in c.execute("PRAGMA table_info(subjects)").fetchall()]
topic_cols = [r[1] for r in c.execute("PRAGMA table_info(topics)").fetchall()]

print("Subjects columns:", subj_cols)
print("Topics columns:", topic_cols)
conn.close()
