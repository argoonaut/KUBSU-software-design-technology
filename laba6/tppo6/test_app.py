import unittest
import sqlite3
from main import Application
from tkinter import Tk
from database import create_tables, insert_sample_data


class TestApp(unittest.TestCase):

    def setUp(self):
        # Создание базы данных для тестирования
        self.conn = sqlite3.connect(":memory:")
        create_tables(self.conn)
        insert_sample_data(self.conn)

        self.root = Tk()
        self.app = Application(self.root, self.conn)

    def tearDown(self):
        self.conn.close()
        self.root.destroy()

    def test_instructors_tab(self):
        # Добавление нового преподавателя
        self.app.instructors_frame.instructor_first_name_entry.insert(0, "Иван")
        self.app.instructors_frame.instructor_last_name_entry.insert(0, "Иванов")
        self.app.instructors_frame.instructor_middle_name_entry.insert(0, "Иванович")
        self.app.instructors_frame.add_instructor_button.invoke()

        # Проверка, что новый преподаватель добавлен в список
        last_instructor = self.app.instructors_frame.instructors_listbox.get(
            self.app.instructors_frame.instructors_listbox.size() - 1)
        self.assertEqual(last_instructor, "Иванов Иван Иванович")

        # Удаление преподавателя
        self.app.instructors_frame.instructors_listbox.selection_set(0)
        self.app.instructors_frame.delete_instructor_button.invoke()

        # Проверка, что преподаватель был удален
        deleted_instructor = self.app.instructors_frame.instructors_listbox.get(0)
        self.assertNotEqual(deleted_instructor, "Иванов Иван Иванович")


if __name__ == "__main__":
    unittest.main()
