import sqlite3
import os
from datetime import datetime

class Database:
    """Класс для работы с базой данных SQLite"""
    
    def __init__(self, db_name='university.db'):
        """
        Инициализация подключения к базе данных
        
        Параметры:
        db_name (str): имя файла базы данных
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()
        self.populate_sample_data()
    
    def connect(self):
        """Подключение к базе данных"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"✓ Подключение к базе данных '{self.db_name}' успешно")
        except sqlite3.Error as e:
            print(f"✗ Ошибка подключения: {e}")
    
    def create_table(self):
        """Создание таблицы students, если её нет"""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    birth_date DATE,
                    group_name TEXT,
                    average_grade REAL
                )
            ''')
            self.conn.commit()
            print("✓ Таблица 'students' готова")
        except sqlite3.Error as e:
            print(f"✗ Ошибка при создании таблицы: {e}")
    
    def populate_sample_data(self):
        """Заполнение таблицы тестовыми данными при первом запуске"""
        try:
            # Проверяем, есть ли уже данные
            self.cursor.execute('SELECT COUNT(*) FROM students')
            count = self.cursor.fetchone()[0]
            
            if count == 0:
                # Тестовые данные
                sample_data = [
                    ('Иван', 'Петров', '2005-03-15', 'ПИ-21', 4.5),
                    ('Мария', 'Сидорова', '2004-07-22', 'ПИ-21', 4.8),
                    ('Алексей', 'Иванов', '2005-01-10', 'ПИ-20', 3.9),
                    ('Елена', 'Кузнецова', '2004-11-05', 'ПИ-20', 4.2),
                    ('Дмитрий', 'Морозов', '2005-05-30', 'ПИ-21', 3.7),
                    ('Анна', 'Волкова', '2004-09-12', 'ПИ-22', 4.6),
                    ('Петр', 'Лебедев', '2005-02-28', 'ПИ-22', 4.0),
                    ('Ольга', 'Соколова', '2004-12-18', 'ПИ-20', 4.1)
                ]
                
                self.cursor.executemany('''
                    INSERT INTO students (first_name, last_name, birth_date, group_name, average_grade)
                    VALUES (?, ?, ?, ?, ?)
                ''', sample_data)
                
                self.conn.commit()
                print(f"✓ Добавлено {len(sample_data)} тестовых записей")
        except sqlite3.Error as e:
            print(f"✗ Ошибка при добавлении данных: {e}")
    
    def get_all_records(self):
        """Получить все записи из таблицы"""
        try:
            self.cursor.execute('SELECT * FROM students ORDER BY id')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ Ошибка при получении записей: {e}")
            return []
    
    def insert_record(self, first_name, last_name, birth_date, group_name, average_grade):
        """Добавить новую запись"""
        try:
            self.cursor.execute('''
                INSERT INTO students (first_name, last_name, birth_date, group_name, average_grade)
                VALUES (?, ?, ?, ?, ?)
            ''', (first_name, last_name, birth_date, group_name, average_grade))
            self.conn.commit()
            print(f"✓ Запись добавлена с ID: {self.cursor.lastrowid}")
            return True
        except sqlite3.Error as e:
            print(f"✗ Ошибка при добавлении записи: {e}")
            return False
    
    def update_record(self, record_id, first_name, last_name, birth_date, group_name, average_grade):
        """Обновить запись"""
        try:
            self.cursor.execute('''
                UPDATE students
                SET first_name=?, last_name=?, birth_date=?, group_name=?, average_grade=?
                WHERE id=?
            ''', (first_name, last_name, birth_date, group_name, average_grade, record_id))
            self.conn.commit()
            print(f"✓ Запись ID {record_id} обновлена")
            return True
        except sqlite3.Error as e:
            print(f"✗ Ошибка при обновлении записи: {e}")
            return False
    
    def delete_record(self, record_id):
        """Удалить запись"""
        try:
            self.cursor.execute('DELETE FROM students WHERE id=?', (record_id,))
            self.conn.commit()
            print(f"✓ Запись ID {record_id} удалена")
            return True
        except sqlite3.Error as e:
            print(f"✗ Ошибка при удалении записи: {e}")
            return False
    
    def close(self):
        """Закрыть соединение с БД"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            print("✓ Соединение с БД закрыто")
        except sqlite3.Error as e:
            print(f"✗ Ошибка при закрытии соединения: {e}")