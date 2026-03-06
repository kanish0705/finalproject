import sqlite3

def get_connection():
    return sqlite3.connect("campus.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department TEXT,
            semester INTEGER,
            section TEXT,
            day TEXT,
            start_time TEXT,
            end_time TEXT,
            subject TEXT,
            faculty TEXT,
            room TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            department TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_dummy_data():
    conn = get_connection()
    cursor = conn.cursor()
    data = [
        ("BCA", 3, "A", "Monday", "09:00", "10:00", "Data Structures", "Dr. Sharma", "Lab 1"),
        ("BCA", 3, "A", "Monday", "10:00", "11:00", "Database Systems", "Prof. Verma", "Room 201"),
        ("BCA", 3, "A", "Tuesday", "09:00", "10:00", "Operating Systems", "Dr. Gupta", "Room 202"),
        ("BCA", 3, "A", "Tuesday", "11:00", "12:00", "Computer Networks", "Prof. Singh", "Lab 2"),
        ("BCA", 3, "A", "Wednesday", "10:00", "11:00", "Data Structures", "Dr. Sharma", "Lab 1"),
        ("BCA", 3, "A", "Wednesday", "14:00", "15:00", "Web Development", "Prof. Kumar", "Lab 3"),
        ("BCA", 3, "A", "Thursday", "09:00", "10:00", "Database Systems", "Prof. Verma", "Room 201"),
        ("BCA", 3, "A", "Thursday", "11:00", "12:00", "Mathematics", "Dr. Patel", "Room 101"),
        ("BCA", 3, "A", "Friday", "10:00", "11:00", "Operating Systems", "Dr. Gupta", "Room 202"),
        ("BCA", 3, "A", "Friday", "14:00", "15:00", "Computer Networks", "Prof. Singh", "Lab 2"),
    ]
    cursor.executemany('''
        INSERT INTO timetable (department, semester, section, day, start_time, end_time, subject, faculty, room)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    insert_dummy_data()
    print("Database initialized with dummy data.")
