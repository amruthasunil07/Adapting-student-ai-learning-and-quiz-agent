import sqlite3

def migrate():
    conn = sqlite3.connect("app.db")
    c = conn.cursor()

    # 1. Inspect existing columns
    subj_cols = [r[1] for r in c.execute("PRAGMA table_info(subjects)").fetchall()]
    topic_cols = [r[1] for r in c.execute("PRAGMA table_info(topics)").fetchall()]

    print("Initial Subjects columns:", subj_cols)
    print("Initial Topics columns:", topic_cols)

    # 2. Add columns to subjects if missing
    if "student_id" not in subj_cols:
        print("[+] Adding student_id to subjects table...")
        c.execute("ALTER TABLE subjects ADD COLUMN student_id INTEGER REFERENCES students(id)")
    
    if "code" not in subj_cols:
        print("[+] Adding code to subjects table...")
        c.execute("ALTER TABLE subjects ADD COLUMN code VARCHAR(50) DEFAULT ''")

    if "semester" not in subj_cols:
        print("[+] Adding semester to subjects table...")
        c.execute("ALTER TABLE subjects ADD COLUMN semester INTEGER DEFAULT 1")

    # 3. Add columns to topics if missing
    if "description" not in topic_cols:
        print("[+] Adding description to topics table...")
        c.execute("ALTER TABLE topics ADD COLUMN description TEXT DEFAULT ''")

    if "priority" not in topic_cols:
        print("[+] Adding priority to topics table...")
        c.execute("ALTER TABLE topics ADD COLUMN priority VARCHAR(20) DEFAULT 'Medium'")

    # 3b. Add explanation column to questions if missing
    q_cols = [r[1] for r in c.execute("PRAGMA table_info(questions)").fetchall()]
    if "explanation" not in q_cols:
        print("[+] Adding explanation to questions table...")
        c.execute("ALTER TABLE questions ADD COLUMN explanation TEXT DEFAULT ''")

    # 4. Associate initial seeded subjects with demo student (id=2) and assign sample codes
    c.execute("UPDATE subjects SET student_id = 2 WHERE student_id IS NULL AND id = 1")
    c.execute("UPDATE subjects SET code = '24CS201', semester = 3 WHERE id = 1 AND (code IS NULL OR code = '')")

    c.execute("UPDATE subjects SET student_id = 2 WHERE student_id IS NULL AND id = 2")
    c.execute("UPDATE subjects SET code = '24ADT301', semester = 3 WHERE id = 2 AND (code IS NULL OR code = '')")

    c.execute("UPDATE subjects SET student_id = 2 WHERE student_id IS NULL AND id = 3")
    c.execute("UPDATE subjects SET code = '24CS302', semester = 4 WHERE id = 3 AND (code IS NULL OR code = '')")

    conn.commit()

    updated_subj_cols = [r[1] for r in c.execute("PRAGMA table_info(subjects)").fetchall()]
    updated_topic_cols = [r[1] for r in c.execute("PRAGMA table_info(topics)").fetchall()]
    print("Updated Subjects columns:", updated_subj_cols)
    print("Updated Topics columns:", updated_topic_cols)

    conn.close()
    print("Migration finished successfully.")

if __name__ == "__main__":
    migrate()
