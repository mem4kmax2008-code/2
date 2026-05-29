import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from datetime import datetime

class StudentManagementApp:
    """Приложение для управления данными студентов"""
    
    def __init__(self, root):
        """
        Инициализация приложения
        
        Параметры:
        root: корневое окно Tkinter
        """
        self.root = root
        self.root.title("Управление данными студентов")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Инициализация БД
        self.db = Database('university.db')
        
        # Переменные состояния
        self.records = []
        self.current_index = 0
        self.add_mode = False
        
        # Загружаем данные
        self.load_records()
        
        # Создаем интерфейс
        self.create_ui()
        
        # Отображаем первую запись
        if self.records:
            self.display_record()
        else:
            self.clear_fields()
            self.update_status()
    
    def create_ui(self):
        """Создание пользовательского интерфейса"""
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Управление записями студентов", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)
        
        # Фрейм с полями ввода
        fields_frame = ttk.LabelFrame(main_frame, text="Данные студента", padding="15")
        fields_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Поле ID (только для чтения)
        ttk.Label(fields_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_id = ttk.Entry(fields_frame, state=tk.DISABLED, width=30)
        self.entry_id.grid(row=0, column=1, sticky=tk.EW, pady=5)
        
        # Имя
        ttk.Label(fields_frame, text="Имя:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_first_name = ttk.Entry(fields_frame, width=30)
        self.entry_first_name.grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        # Фамилия
        ttk.Label(fields_frame, text="Фамилия:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_last_name = ttk.Entry(fields_frame, width=30)
        self.entry_last_name.grid(row=2, column=1, sticky=tk.EW, pady=5)
        
        # Дата рождения
        ttk.Label(fields_frame, text="Дата рождения:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_birth_date = ttk.Entry(fields_frame, width=30)
        self.entry_birth_date.grid(row=3, column=1, sticky=tk.EW, pady=5)
        ttk.Label(fields_frame, text="(ГГГГ-ММ-ДД)", font=('Arial', 8)).grid(row=3, column=2, sticky=tk.W, padx=10)
        
        # Группа
        ttk.Label(fields_frame, text="Группа:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.entry_group = ttk.Entry(fields_frame, width=30)
        self.entry_group.grid(row=4, column=1, sticky=tk.EW, pady=5)
        
        # Средняя оценка
        ttk.Label(fields_frame, text="Средняя оценка:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.entry_avg_grade = ttk.Entry(fields_frame, width=30)
        self.entry_avg_grade.grid(row=5, column=1, sticky=tk.EW, pady=5)
        
        # Настройка ширины столбцов
        fields_frame.columnconfigure(1, weight=1)
        
        # Фрейм навигации
        nav_frame = ttk.LabelFrame(main_frame, text="Навигация", padding="10")
        nav_frame.pack(fill=tk.X, pady=10)
        
        # Кнопки навигации
        button_width = 12
        self.btn_first = ttk.Button(nav_frame, text="⏮ Первая", width=button_width, command=self.goto_first)
        self.btn_first.pack(side=tk.LEFT, padx=5)
        
        self.btn_previous = ttk.Button(nav_frame, text="◀ Предыдущая", width=button_width, command=self.goto_previous)
        self.btn_previous.pack(side=tk.LEFT, padx=5)
        
        self.btn_next = ttk.Button(nav_frame, text="Следующая ▶", width=button_width, command=self.goto_next)
        self.btn_next.pack(side=tk.LEFT, padx=5)
        
        self.btn_last = ttk.Button(nav_frame, text="Последняя ⏭", width=button_width, command=self.goto_last)
        self.btn_last.pack(side=tk.LEFT, padx=5)
        
        # Статусная строка
        self.label_status = ttk.Label(nav_frame, text="Статус: ", font=('Arial', 9))
        self.label_status.pack(side=tk.RIGHT, padx=10)
        
        # Фрейм кнопок управления
        control_frame = ttk.LabelFrame(main_frame, text="Управление", padding="10")
        control_frame.pack(fill=tk.X, pady=10)
        
        self.btn_add = ttk.Button(control_frame, text="➕ Новая запись", width=button_width, command=self.add_new_record)
        self.btn_add.pack(side=tk.LEFT, padx=5)
        
        self.btn_save = ttk.Button(control_frame, text="💾 Сохранить", width=button_width, command=self.save_record)
        self.btn_save.pack(side=tk.LEFT, padx=5)
        
        self.btn_delete = ttk.Button(control_frame, text="🗑️ Удалить", width=button_width, command=self.delete_record)
        self.btn_delete.pack(side=tk.LEFT, padx=5)
        
        self.btn_refresh = ttk.Button(control_frame, text="🔄 Обновить", width=button_width, command=self.refresh_data)
        self.btn_refresh.pack(side=tk.LEFT, padx=5)
        
        # Привязка события закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_records(self):
        """Загрузка записей из БД"""
        self.records = self.db.get_all_records()
        self.current_index = 0
    
    def display_record(self):
        """Отображение текущей записи"""
        if not self.records:
            self.clear_fields()
            self.update_status()
            return
        
        record = self.records[self.current_index]
        
        # Очищаем поля
        self.clear_fields()
        
        # Заполняем поля данными
        self.entry_id.config(state=tk.NORMAL)
        self.entry_id.insert(0, str(record[0]))
        self.entry_id.config(state=tk.DISABLED)
        
        self.entry_first_name.insert(0, record[1])
        self.entry_last_name.insert(0, record[2])
        self.entry_birth_date.insert(0, record[3] or "")
        self.entry_group.insert(0, record[4] or "")
        self.entry_avg_grade.insert(0, str(record[5]) if record[5] else "")
        
        # Обновляем статус
        self.update_status()
        
        # Выходим из режима добавления
        self.add_mode = False
    
    def clear_fields(self):
        """Очистка полей ввода"""
        self.entry_id.config(state=tk.NORMAL)
        self.entry_id.delete(0, tk.END)
        self.entry_id.config(state=tk.DISABLED)
        
        self.entry_first_name.delete(0, tk.END)
        self.entry_last_name.delete(0, tk.END)
        self.entry_birth_date.delete(0, tk.END)
        self.entry_group.delete(0, tk.END)
        self.entry_avg_grade.delete(0, tk.END)
    
    def update_status(self):
        """Обновление статусной строки"""
        if not self.records:
            self.label_status.config(text="Статус: Нет записей")
        elif self.add_mode:
            self.label_status.config(text="Статус: Режим добавления")
        else:
            total = len(self.records)
            current = self.current_index + 1
            self.label_status.config(text=f"Статус: Запись {current} из {total}")
    
    def goto_first(self):
        """Перейти на первую запись"""
        if self.records:
            self.current_index = 0
            self.display_record()
    
    def goto_previous(self):
        """Перейти на предыдущую запись"""
        if self.records and self.current_index > 0:
            self.current_index -= 1
            self.display_record()
    
    def goto_next(self):
        """Перейти на следующую запись"""
        if self.records and self.current_index < len(self.records) - 1:
            self.current_index += 1
            self.display_record()
    
    def goto_last(self):
        """Перейти на последнюю запись"""
        if self.records:
            self.current_index = len(self.records) - 1
            self.display_record()
    
    def add_new_record(self):
        """Режим добавления новой записи"""
        self.clear_fields()
        self.add_mode = True
        self.update_status()
        self.entry_first_name.focus()
    
    def save_record(self):
        """Сохранить запись (INSERT или UPDATE)"""
        # Получаем данные из полей
        first_name = self.entry_first_name.get().strip()
        last_name = self.entry_last_name.get().strip()
        birth_date = self.entry_birth_date.get().strip()
        group_name = self.entry_group.get().strip()
        avg_grade_str = self.entry_avg_grade.get().strip()
        
        # Валидация
        if not first_name or not last_name:
            messagebox.showwarning("Ошибка валидации", "Имя и фамилия обязательны!")
            return
        
        # Проверяем оценку
        try:
            avg_grade = float(avg_grade_str) if avg_grade_str else None
            if avg_grade and (avg_grade < 0 or avg_grade > 5):
                messagebox.showwarning("Ошибка валидации", "Оценка должна быть от 0 до 5!")
                return
        except ValueError:
            messagebox.showwarning("Ошибка валидации", "Оценка должна быть числом!")
            return
        
        # Проверяем дату
        if birth_date:
            try:
                datetime.strptime(birth_date, '%Y-%m-%d')
            except ValueError:
                messagebox.showwarning("Ошибка вали��ации", "Неверный формат даты (ГГГГ-ММ-ДД)!")
                return
        
        if self.add_mode:
            # Режим добавления
            if self.db.insert_record(first_name, last_name, birth_date, group_name, avg_grade):
                messagebox.showinfo("Успешно", "Запись добавлена!")
                self.refresh_data()
                self.goto_last()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить запись")
        else:
            # Режим обновления
            record_id = int(self.entry_id.get())
            if self.db.update_record(record_id, first_name, last_name, birth_date, group_name, avg_grade):
                messagebox.showinfo("Успешно", "Запись обновлена!")
                self.refresh_data()
                # Восстанавливаем позицию
                self.current_index = min(self.current_index, len(self.records) - 1)
                if self.records:
                    self.display_record()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить запись")
    
    def delete_record(self):
        """Удалить текущую запись"""
        if not self.records:
            messagebox.showwarning("Предупреждение", "Нет записей для удаления")
            return
        
        record_id = int(self.entry_id.get())
        student_name = f"{self.entry_first_name.get()} {self.entry_last_name.get()}"
        
        # Запрашиваем подтверждение
        if messagebox.askyesno("Подтверждение", f"Удалить запись '{student_name}'?"):
            if self.db.delete_record(record_id):
                messagebox.showinfo("Успешно", "Запись удалена!")
                self.refresh_data()
                
                # Корректируем индекс
                if self.records:
                    if self.current_index >= len(self.records):
                        self.current_index = len(self.records) - 1
                    self.display_record()
                else:
                    self.clear_fields()
                    self.update_status()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить запись")
    
    def refresh_data(self):
        """Обновить данные из БД"""
        self.load_records()
        if self.records:
            self.current_index = min(self.current_index, len(self.records) - 1)
            self.display_record()
        else:
            self.clear_fields()
            self.update_status()
        messagebox.showinfo("Успешно", "Данные обновлены")
    
    def on_closing(self):
        """Обработчик закрытия окна"""
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            self.db.close()
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop()