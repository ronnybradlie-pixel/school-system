import sqlite3
import customtkinter as ctk

conn =sqlite3.connect('school.db')
cursor =conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    class_name TEXT
)
""") 
conn.commit()

# OOP\database creation
class Student:
    def __init__(self,name,class_name):
        self.name = name 
        self.class_name =class_name
    
    def save(self):
        cursor.execute("INSERT INTO students (name, class_name) VALUES (?, ?)",
            (self.name, self.class_name)    
        )
        conn.commit()
        print("Student saved successfully!")

        # students function
    # def add_student():
    #         name = input('enter student name')
    #         class_name = input('enter class')
    #         student = Student(name, class_name)
    #         student.save()
    
    def view_Students():
         cursor.execute('SELECT * FROM students')
         Student = cursor.fetchall()

    




