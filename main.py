import customtkinter as ctk
from database import StudentDatabase
from tkinter import messagebox, simpledialog
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SchoolManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System")
        self.root.geometry("700x600")
        self.db = StudentDatabase()
        
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        # Header
        header = ctk.CTkLabel(self.root, text="School Management System", font=("Arial", 24, "bold"))
        header.pack(pady=20)

        # Frame for buttons
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=10)

        # Buttons
        ctk.CTkButton(button_frame, text="Add Student", command=self.add_student_dialog, width=150).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkButton(button_frame, text="View Students", command=self.view_students, width=150).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(button_frame, text="Search Student", command=self.search_dialog, width=150).grid(row=1, column=0, padx=5, pady=5)
        ctk.CTkButton(button_frame, text="Update Student", command=self.update_dialog, width=150).grid(row=1, column=1, padx=5, pady=5)
        ctk.CTkButton(button_frame, text="Delete Student", command=self.delete_dialog, width=150).grid(row=2, column=0, padx=5, pady=5)
        ctk.CTkButton(button_frame, text="Exit", command=self.exit_app, width=150).grid(row=2, column=1, padx=5, pady=5)

        # Text widget for displaying results
        self.text_widget = ctk.CTkTextbox(self.root, width=650, height=350)
        self.text_widget.pack(pady=10, padx=20)
        self.text_widget.configure(state="disabled")

    def add_student_dialog(self):
        """Dialog to add a new student"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Add Student")
        dialog.geometry("300x200")
        dialog.resizable(False, False)

        ctk.CTkLabel(dialog, text="Name:").pack(pady=10)
        name_entry = ctk.CTkEntry(dialog, width=200)
        name_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Class:").pack(pady=10)
        class_entry = ctk.CTkEntry(dialog, width=200)
        class_entry.pack(pady=5)

        def save():
            try:
                name = name_entry.get().strip()
                class_name = class_entry.get().strip()
                
                if not name or not class_name:
                    messagebox.showerror("Error", "Name and class cannot be empty!")
                    return
                
                self.db.add_student(name, class_name)
                messagebox.showinfo("Success", "Student added successfully!")
                dialog.destroy()
                self.view_students()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(dialog, text="Save", command=save).pack(pady=20)

    def view_students(self):
        """Display all students"""
        try:
            students = self.db.get_all_students()
            self.update_text_widget("All Students\n" + "="*50 + "\n")
            
            if not students:
                self.append_text("No students found.\n")
            else:
                for s in students:
                    self.append_text(f"ID: {s[0]}\nName: {s[1]}\nClass: {s[2]}\n{'-'*50}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_dialog(self):
        """Dialog to search for a student"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Search Student")
        dialog.geometry("300x150")
        dialog.resizable(False, False)

        ctk.CTkLabel(dialog, text="Enter student name:").pack(pady=10)
        search_entry = ctk.CTkEntry(dialog, width=200)
        search_entry.pack(pady=5)

        def search():
            try:
                name = search_entry.get().strip()
                if not name:
                    messagebox.showerror("Error", "Please enter a name to search!")
                    return
                
                results = self.db.search_student(name)
                self.update_text_widget(f"Search Results for '{name}'\n" + "="*50 + "\n")
                
                if not results:
                    self.append_text("No students found with that name.\n")
                else:
                    for s in results:
                        self.append_text(f"ID: {s[0]}\nName: {s[1]}\nClass: {s[2]}\n{'-'*50}\n")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(dialog, text="Search", command=search).pack(pady=10)

    def update_dialog(self):
        """Dialog to update a student"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Update Student")
        dialog.geometry("300x250")
        dialog.resizable(False, False)

        ctk.CTkLabel(dialog, text="Student ID:").pack(pady=10)
        id_entry = ctk.CTkEntry(dialog, width=200)
        id_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="New Name:").pack(pady=10)
        name_entry = ctk.CTkEntry(dialog, width=200)
        name_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="New Class:").pack(pady=10)
        class_entry = ctk.CTkEntry(dialog, width=200)
        class_entry.pack(pady=5)

        def update():
            try:
                student_id = id_entry.get().strip()
                name = name_entry.get().strip()
                class_name = class_entry.get().strip()
                
                if not student_id or not name or not class_name:
                    messagebox.showerror("Error", "All fields are required!")
                    return
                
                student = self.db.get_student_by_id(int(student_id))
                if not student:
                    messagebox.showerror("Error", f"No student found with ID {student_id}!")
                    return
                
                self.db.update_student(int(student_id), name, class_name)
                messagebox.showinfo("Success", "Student updated successfully!")
                dialog.destroy()
                self.view_students()
            except ValueError:
                messagebox.showerror("Error", "Invalid student ID!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(dialog, text="Update", command=update).pack(pady=10)

    def delete_dialog(self):
        """Dialog to delete a student"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Delete Student")
        dialog.geometry("300x150")
        dialog.resizable(False, False)

        ctk.CTkLabel(dialog, text="Enter Student ID:").pack(pady=10)
        id_entry = ctk.CTkEntry(dialog, width=200)
        id_entry.pack(pady=5)

        def delete():
            try:
                student_id = id_entry.get().strip()
                if not student_id:
                    messagebox.showerror("Error", "Please enter a student ID!")
                    return
                
                student = self.db.get_student_by_id(int(student_id))
                if not student:
                    messagebox.showerror("Error", f"No student found with ID {student_id}!")
                    return
                
                if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
                    self.db.delete_student(int(student_id))
                    messagebox.showinfo("Success", "Student deleted successfully!")
                    dialog.destroy()
                    self.view_students()
            except ValueError:
                messagebox.showerror("Error", "Invalid student ID!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(dialog, text="Delete", command=delete).pack(pady=10)

    def update_text_widget(self, text):
        """Update text widget content"""
        self.text_widget.configure(state="normal")
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", text)
        self.text_widget.configure(state="disabled")

    def append_text(self, text):
        """Append text to text widget"""
        self.text_widget.configure(state="normal")
        self.text_widget.insert(tk.END, text)
        self.text_widget.configure(state="disabled")

    def exit_app(self):
        """Close the application"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.db.close()
            self.root.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    app = SchoolManagementApp(root)
    root.mainloop()
