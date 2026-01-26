import sqlite3
from typing import List, Tuple, Optional

class StudentDatabase:
    def __init__(self, db_name: str = 'school.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.initialize()

    def initialize(self):
        """Initialize database connection and create table if needed"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.create_table()
        except sqlite3.Error as e:
            raise Exception(f"Database connection error: {e}")

    def create_table(self):
        """Create students table if it doesn't exist"""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    class_name TEXT NOT NULL
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Error creating table: {e}")

    def add_student(self, name: str, class_name: str) -> bool:
        """Add a new student to the database"""
        try:
            if not name or not class_name:
                raise ValueError("Name and class cannot be empty")
            
            self.cursor.execute(
                "INSERT INTO students (name, class_name) VALUES (?, ?)",
                (name.strip(), class_name.strip())
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            raise Exception(f"Error adding student: {e}")

    def get_all_students(self) -> List[Tuple]:
        """Get all students from database"""
        try:
            self.cursor.execute("SELECT * FROM students")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Error fetching students: {e}")

    def search_student(self, name: str) -> List[Tuple]:
        """Search for students by name"""
        try:
            self.cursor.execute(
                "SELECT * FROM students WHERE name LIKE ?",
                (f'%{name}%',)
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Error searching students: {e}")

    def update_student(self, student_id: int, name: str, class_name: str) -> bool:
        """Update student information"""
        try:
            if not name or not class_name:
                raise ValueError("Name and class cannot be empty")
            
            self.cursor.execute(
                "UPDATE students SET name = ?, class_name = ? WHERE id = ?",
                (name.strip(), class_name.strip(), student_id)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            raise Exception(f"Error updating student: {e}")

    def delete_student(self, student_id: int) -> bool:
        """Delete a student from database"""
        try:
            self.cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            raise Exception(f"Error deleting student: {e}")

    def get_student_by_id(self, student_id: int) -> Optional[Tuple]:
        """Get a specific student by ID"""
        try:
            self.cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            raise Exception(f"Error fetching student: {e}")

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()