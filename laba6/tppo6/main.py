import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import os
from database import connect_to_db, create_tables
import time

start_time = time.time()
conn = connect_to_db()
cursor = conn.cursor()
create_tables(cursor)

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("ТППО")
        self.geometry("800x600")
        self.resizable(False, False)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self.instructor_tab = InstructorTab(self.notebook)
        self.course_tab = CourseTab(self.notebook)
        self.cashier_tab = CashierTab(self.notebook)
        self.client_tab = ClientTab(self.notebook)

        self.notebook.add(self.instructor_tab, text="Преподаватели")
        self.notebook.add(self.course_tab, text="Курсы")
        self.notebook.add(self.cashier_tab, text="Кассиры")
        self.notebook.add(self.client_tab, text="Клиенты")

        self.print_receipt_button = ttk.Button(self, text="Напечатать чек", command=self.print_receipt)
        self.print_receipt_button.pack(side=tk.BOTTOM, pady=10)

    def print_receipt(self):
        # Получение всех таблиц из базы данных
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Создание объекта Excel-файла с несколькими листами
        writer = pd.ExcelWriter("database_export.xlsx", engine='xlsxwriter')

        # Экспорт каждой таблицы в отдельный лист Excel
        for table_name in tables:
            table_name = table_name[0]
            cursor.execute(f"SELECT * FROM {table_name};")
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()

            if data:
                df = pd.DataFrame(data, columns=columns)
                df.to_excel(writer, sheet_name=table_name, index=False)

        # Сохранение Excel-файла
        writer.close()
        messagebox.showinfo("Успешно", f"База данных экспортирована в файл 'database_export.xlsx'")

class ClientTab(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Создаем виджеты
        self.create_widgets()

    def create_widgets(self):
        # Виджеты для отображения списка клиентов
        self.client_list = ttk.Treeview(self)
        self.client_list["columns"] = ("FirstName", "LastName", "PhoneNumber", "Email")
        self.client_list.column("#0", width=50, stretch=tk.NO)
        self.client_list.heading("#0", text="ID")
        self.client_list.column("FirstName", width=100, anchor=tk.W)
        self.client_list.heading("FirstName", text="Имя")
        self.client_list.column("LastName", width=100, anchor=tk.W)
        self.client_list.heading("LastName", text="Фамилия")
        self.client_list.column("PhoneNumber", width=100, anchor=tk.W)
        self.client_list.heading("PhoneNumber", text="Телефон")
        self.client_list.column("Email", width=150, anchor=tk.W)
        self.client_list.heading("Email", text="Email")

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.client_list.yview)
        self.client_list.configure(yscroll=self.scrollbar.set)

        # Виджеты для добавления новых клиентов
        self.form_frame = ttk.Frame(self)
        self.first_name_label = ttk.Label(self.form_frame, text="Имя:")
        self.first_name_entry = ttk.Entry(self.form_frame)
        self.last_name_label = ttk.Label(self.form_frame, text="Фамилия:")
        self.last_name_entry = ttk.Entry(self.form_frame)
        self.phone_number_label = ttk.Label(self.form_frame, text="Телефон:")
        self.phone_number_entry = ttk.Entry(self.form_frame)
        self.email_label = ttk.Label(self.form_frame, text="Email:")
        self.email_entry = ttk.Entry(self.form_frame)

        self.add_button = ttk.Button(self.form_frame, text="Добавить", command=self.add_client)
        self.delete_button = ttk.Button(self.form_frame, text="Удалить", command=self.delete_client)


        # Расп
        self.client_list.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.form_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.first_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.first_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.last_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.last_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.phone_number_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.phone_number_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.email_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.email_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.add_button.grid(row=4, column=0, padx=5, pady=5)
        self.delete_button.grid(row=4, column=1, padx=5, pady=5)

        self.load_clients()

    def load_clients(self):
        cursor.execute("SELECT * FROM Clients")
        clients = cursor.fetchall()

        self.client_list.delete(*self.client_list.get_children())
        for client in clients:
            self.client_list.insert("", tk.END, iid=client[0], text=client[0],
                                    values=(client[1], client[2], client[3], client[4]))

    def add_client(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone_number = self.phone_number_entry.get()
        email = self.email_entry.get()

        if not first_name or not last_name or not phone_number or not email:
            # Выводим сообщение об ошибке, если обязательные поля не заполнены
            tk.messagebox.showerror("Ошибка", "Пожалуйста, заполните обязательные поля.")
        else:
            cursor.execute("INSERT INTO Clients (FirstName, LastName, PhoneNumber, Email) VALUES (?, ?, ?, ?)",
                           (first_name, last_name, phone_number, email))
            conn.commit()
            self.load_clients()
            self.clear_form()

    def delete_client(self):
        selected_item = self.client_list.focus()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Пожалуйста, выберите клиента для удаления.")
            return

        cursor.execute("DELETE FROM Clients WHERE ID=?", (selected_item,))
        conn.commit()
        self.load_clients()
        self.clear_form()

    def clear_form(self):
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.phone_number_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

class CashierTab(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Создаем виджеты
        self.create_widgets()

    def create_widgets(self):
        # Виджеты для отображения списка кассиров
        self.cashier_list = ttk.Treeview(self)
        self.cashier_list["columns"] = ("FirstName", "LastName", "MiddleName", "MachineID")
        self.cashier_list.column("#0", width=50, stretch=tk.NO)
        self.cashier_list.heading("#0", text="ID")
        self.cashier_list.column("FirstName", width=100, anchor=tk.W)
        self.cashier_list.heading("FirstName", text="Имя")
        self.cashier_list.column("LastName", width=100, anchor=tk.W)
        self.cashier_list.heading("LastName", text="Фамилия")
        self.cashier_list.column("MiddleName", width=100, anchor=tk.W)
        self.cashier_list.heading("MiddleName", text="Отчество")
        self.cashier_list.column("MachineID", width=100, anchor=tk.W)
        self.cashier_list.heading("MachineID", text="ID машины")

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.cashier_list.yview)
        self.cashier_list.configure(yscroll=self.scrollbar.set)

        # Виджеты для добавления новых кассиров
        self.form_frame = ttk.Frame(self)
        self.first_name_label = ttk.Label(self.form_frame, text="Имя:")
        self.first_name_entry = ttk.Entry(self.form_frame)
        self.last_name_label = ttk.Label(self.form_frame, text="Фамилия:")
        self.last_name_entry = ttk.Entry(self.form_frame)
        self.middle_name_label = ttk.Label(self.form_frame, text="Отчество:")
        self.middle_name_entry = ttk.Entry(self.form_frame)
        self.machine_id_label = ttk.Label(self.form_frame, text="ID машины:")
        self.machine_id_entry = ttk.Entry(self.form_frame)

        self.add_button = ttk.Button(self.form_frame, text="Добавить", command=self.add_cashier)
        self.delete_button = ttk.Button(self.form_frame, text="Удалить", command=self.delete_cashier)


        self.cashier_list.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.form_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.first_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.first_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.last_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.last_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.middle_name_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.middle_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.machine_id_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.machine_id_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.add_button.grid(row=4, column=0, padx=5, pady=5)
        self.delete_button.grid(row=4, column=1, padx=5, pady=5)

        self.load_cashiers()

    def load_cashiers(self):
        cursor.execute("SELECT * FROM Cashiers")
        cashiers = cursor.fetchall()

        self.cashier_list.delete(*self.cashier_list.get_children())
        for cashier in cashiers:
            self.cashier_list.insert("", tk.END, iid=cashier[0], text=cashier[0],
                                     values=(cashier[1], cashier[2], cashier[3], cashier[4]))

    def add_cashier(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        middle_name = self.middle_name_entry.get()
        machine_id = self.machine_id_entry.get()

        if not first_name or not last_name or not machine_id:
            # Выводим сообщение об ошибке, если обязательные поля не заполнены
            tk.messagebox.showerror("Ошибка", "Пожалуйста, заполните обязательные поля.")
        else:
            cursor.execute("INSERT INTO Cashiers (FirstName, LastName, MiddleName, MachineID) VALUES (?, ?, ?, ?)",
                           (first_name, last_name, middle_name, machine_id))
            conn.commit()
            self.load_cashiers()
            self.clear_form()

    def delete_cashier(self):
        selected_item = self.cashier_list.focus()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Пожалуйста, выберите кассира для удаления.")
            return

        cursor.execute("DELETE FROM Cashiers WHERE ID=?", (selected_item,))
        conn.commit()
        self.load_cashiers()
        self.clear_form()

    def clear_form(self):
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.middle_name_entry.delete(0, tk.END)
        self.machine_id_entry.delete(0, tk.END)

class CourseTab(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Создаем виджеты
        self.create_widgets()

    def create_widgets(self):
        # Виджеты для отображения списка курсов
        self.course_list = ttk.Treeview(self)
        self.course_list["columns"] = ("Name", "Price", "Description", "IsReady")
        self.course_list.column("#0", width=50, stretch=tk.NO)
        self.course_list.heading("#0", text="ID")
        self.course_list.column("Name", width=100, anchor=tk.W)
        self.course_list.heading("Name", text="Название")
        self.course_list.column("Price", width=100, anchor=tk.W)
        self.course_list.heading("Price", text="Цена")
        self.course_list.column("Description", width=100, anchor=tk.W)
        self.course_list.heading("Description", text="Описание")
        self.course_list.column("IsReady", width=100, anchor=tk.W)
        self.course_list.heading("IsReady", text="Готовность")

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.course_list.yview)
        self.course_list.configure(yscroll=self.scrollbar.set)

        # Виджеты для добавления новых курсов
        self.form_frame = ttk.Frame(self)
        self.name_label = ttk.Label(self.form_frame, text="Название:")
        self.name_entry = ttk.Entry(self.form_frame)
        self.price_label = ttk.Label(self.form_frame, text="Цена:")
        self.price_entry = ttk.Entry(self.form_frame)
        self.description_label = ttk.Label(self.form_frame, text="Описание:")
        self.description_entry = ttk.Entry(self.form_frame)
        self.is_ready_label = ttk.Label(self.form_frame, text="Готовность:")
        self.is_ready_var = tk.BooleanVar()
        self.is_ready_checkbutton = ttk.Checkbutton(self.form_frame, variable=self.is_ready_var)

        self.add_button = ttk.Button(self.form_frame, text="Добавить", command=self.add_course)
        self.delete_button = ttk.Button(self.form_frame, text="Удалить", command=self.delete_course)


        # Расположение виджетов на экран
        self.course_list.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.form_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.price_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.price_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.description_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.description_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.is_ready_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.is_ready_checkbutton.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.add_button.grid(row=4, column=0, padx=5, pady=5)
        self.delete_button.grid(row=4, column=1, padx=5, pady=5)

        self.load_courses()

    def load_courses(self):
        cursor.execute("SELECT * FROM Courses")
        courses = cursor.fetchall()

        self.course_list.delete(*self.course_list.get_children())
        for course in courses:
            is_ready_text = "Готов" if course[4] else "Не готов"
            self.course_list.insert("", tk.END, iid=course[0], text=course[0],
                                    values=(course[1], course[2], course[3], is_ready_text))

    def add_course(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        description = self.description_entry.get()
        is_ready = self.is_ready_var.get()

        if not name or not price:
            # Выводим сообщение об ошибке, если обязательные поля не заполнены
            tk.messagebox.showerror("Ошибка", "Пожалуйста, заполните обязательные поля.")
        else:
            cursor.execute("INSERT INTO Courses (Name, Price, Description, IsReady) VALUES (?, ?, ?, ?)",
                           (name, price, description, is_ready))
            conn.commit()
            self.load_courses()
            self.clear_form()

    def delete_course(self):
        selected_item = self.course_list.focus()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Пожалуйста, выберите курс для удаления.")
            return

        cursor.execute("DELETE FROM Courses WHERE ID=?", (selected_item,))
        conn.commit()
        self.load_courses()
        self.clear_form()

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.is_ready_var.set(False)

class InstructorTab(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Создаем виджеты
        self.create_widgets()

    def create_widgets(self):
        # Виджеты для отображения списка преподавателей
        self.instructor_list = ttk.Treeview(self)
        self.instructor_list["columns"] = ("FirstName", "LastName", "MiddleName", "CourseID")
        self.instructor_list.column("#0", width=50, stretch=tk.NO)
        self.instructor_list.heading("#0", text="ID")
        self.instructor_list.column("FirstName", width=100, anchor=tk.W)
        self.instructor_list.heading("FirstName", text="Имя")
        self.instructor_list.column("LastName", width=100, anchor=tk.W)
        self.instructor_list.heading("LastName", text="Фамилия")
        self.instructor_list.column("MiddleName", width=100, anchor=tk.W)
        self.instructor_list.heading("MiddleName", text="Отчество")
        self.instructor_list.column("CourseID", width=100, anchor=tk.W)
        self.instructor_list.heading("CourseID", text="ID курса")

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.instructor_list.yview)
        self.instructor_list.configure(yscroll=self.scrollbar.set)

        # Виджеты для добавления новых преподавателей
        self.form_frame = ttk.Frame(self)
        self.first_name_label = ttk.Label(self.form_frame, text="Имя:")
        self.first_name_entry = ttk.Entry(self.form_frame)
        self.last_name_label = ttk.Label(self.form_frame, text="Фамилия:")
        self.last_name_entry = ttk.Entry(self.form_frame)
        self.middle_name_label = ttk.Label(self.form_frame, text="Отчество:")
        self.middle_name_entry = ttk.Entry(self.form_frame)
        self.course_id_label = ttk.Label(self.form_frame, text="ID курса:")
        self.course_id_entry = ttk.Entry(self.form_frame)

        self.add_button = ttk.Button(self.form_frame, text="Добавить", command=self.add_instructor)
        self.delete_button = ttk.Button(self.form_frame, text="Удалить", command=self.delete_instructor)

        # Расположение виджетов на экране
        self.instructor_list.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.form_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.first_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.first_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.last_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.last_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.middle_name_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.middle_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.course_id_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.course_id_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.add_button.grid(row=4, column=0, padx=5, pady=5)
        self.delete_button.grid(row=4, column=1, padx=5, pady=5)

        self.load_instructors()

    def load_instructors(self):
        cursor.execute("SELECT * FROM Instructors")
        instructors = cursor.fetchall()

        self.instructor_list.delete(*self.instructor_list.get_children())
        for instructor in instructors:
            self.instructor_list.insert("", tk.END, iid=instructor[0], text=instructor[0],
                                        values=(instructor[1], instructor[2], instructor[3], instructor[4]))

    def add_instructor(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        middle_name = self.middle_name_entry.get()
        course_id = self.course_id_entry.get()

        if not first_name or not last_name or not course_id:
            # Выводим сообщение об ошибке, если обязательные поля не заполнены
            tk.messagebox.showerror("Ошибка", "Пожалуйста, заполните обязательные поля.")
        else:
            cursor.execute("INSERT INTO Instructors (FirstName, LastName, MiddleName, CourseID) VALUES (?, ?, ?, ?)",
                           (first_name, last_name, middle_name, course_id))
            conn.commit()
            self.load_instructors()
            self.clear_form()

    def delete_instructor(self):
        selected_item = self.instructor_list.focus()
        if not selected_item:
            tk.messagebox.showerror("Ошибка", "Пожалуйста, выберите преподавателя для удаления.")
            return

        cursor.execute("DELETE FROM Instructors WHERE ID=?", (selected_item,))
        conn.commit()
        self.load_instructors()
        self.clear_form()

    def clear_form(self):
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.middle_name_entry.delete(0, tk.END)
        self.course_id_entry.delete(0, tk.END)


if __name__ == "__main__":
    app = Application()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Загрузка оконного приложения заняла: {elapsed_time:.2f} секунд")
    app.mainloop()

