import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sys
import json
import webbrowser

# Файл для хранения данных
DATA_FILE = "config.json"

# Глобальные переменные для запоминания значений
saved_folder_path = ""
saved_word = ""
saved_count = 0
saved_filename = ""


def load_data():
    """Загрузить данные из файла config.json, если они есть."""
    global saved_folder_path, saved_word, saved_count, saved_filename

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
                saved_folder_path = data.get("folder_path", "")
                saved_word = data.get("word", "")
                saved_count = data.get("count", 0)
                saved_filename = data.get("filename", "")
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")


def save_data():
    """Сохранить данные в файл config.json."""
    data = {
        "folder_path": folder_entry.get(),
        "word": word_entry.get(),
        "count": count_entry.get(),
        "filename": filename_entry.get()
    }
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка сохранения данных: {e}")


def select_folder():
    """Открыть диалог выбора папки и установить её путь."""
    folder = filedialog.askdirectory(title="Выберите папку для сохранения файла")
    if folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)


def generate_filename(folder_path, base_name="Повтор"):
    """Генерация уникального имени файла (например, Повтор-1.txt, Повтор-2.txt)."""
    index = 1
    while os.path.exists(os.path.join(folder_path, f"{base_name}-{index}.txt")):
        index += 1
    return f"{base_name}-{index}.txt"


def create_file():
    """Создать файл с указанными параметрами."""
    global saved_folder_path, saved_word, saved_count

    folder_path = folder_entry.get()
    word = word_entry.get()
    file_name = filename_entry.get().strip()
    count_str = count_entry.get()

    # Сохранение значений
    saved_folder_path = folder_path
    saved_word = word
    saved_count = count_str

    # Проверка на пустые поля (кроме имени файла)
    missing_fields = []
    if not folder_path:
        missing_fields.append("Путь")
    if not word:
        missing_fields.append("Слово")
    if not count_str:
        missing_fields.append("Количество повторений")

    # Если есть незаполненные поля, показываем ошибку
    if missing_fields:
        missing_fields_str = ", ".join(missing_fields)
        messagebox.showerror("Ошибка", f"Пожалуйста, заполните следующие поля: {missing_fields_str}.")
        return

    try:
        repeat_count = int(count_str)
    except ValueError:
        messagebox.showerror("Ошибка", "Количество повторений должно быть числом.")
        return

    if not os.path.isdir(folder_path):
        messagebox.showerror("Ошибка", "Выбранный путь недействителен.")
        return

    # Генерация имени файла, если оно не указано
    if not file_name:
        file_name = generate_filename(folder_path)  # Если имя не указано, генерируем автоматическое

    file_path = os.path.join(folder_path, file_name)

    # Сброс полосы прогресса и установка максимума
    progress["value"] = 0
    progress["maximum"] = repeat_count

    # Создание файла и запись данных
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for i in range(repeat_count):
                file.write(word + '\n')

                # Обновление полосы прогресса
                progress["value"] = i + 1
                progress_percentage = (i + 1) / repeat_count * 100
                percent_label.config(text=f"{int(progress_percentage)}%")

                root.update_idletasks()  # Обновление интерфейса

        # После завершения создаем сообщение об успешном создании
        messagebox.showinfo("Успех", f"Файл успешно создан: {file_path}")
        
        # Сохранить данные перед перезапуском
        save_data()

        # Перезапуск программы после закрытия сообщения
        restart_program()

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось создать файл: {e}")


def restart_program():
    """Перезапуск программы с сохранёнными значениями."""
    # Закрытие текущего окна
    root.quit()

    # Повторный запуск программы с сохранёнными значениями
    os.execl(sys.executable, sys.executable, *sys.argv)


def open_author_page():
    """Открыть страницу автора в браузере."""
    webbrowser.open("https://bazipl1.carrd.co/")  # Замените на реальный URL


# Создаём окно приложения
root = tk.Tk()
root.title("Создание файла")
root.geometry("595x290")
root.resizable(False, False)

# Загрузка сохраненных данных
load_data()

# Поля ввода
tk.Label(root, text="Выберите папку:").grid(row=0, column=0, padx=5, pady=5)
folder_entry = tk.Entry(root, width=40)
folder_entry.grid(row=0, column=1, padx=5, pady=5)
folder_entry.insert(0, saved_folder_path)  # Заполняем сохраненным путем
browse_button = tk.Button(root, text="Обзор...", command=select_folder)
browse_button.grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Введите имя файла (по умолчанию Повтор-1):").grid(row=1, column=0, padx=5, pady=5)
filename_entry = tk.Entry(root, width=30)
filename_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2)
filename_entry.insert(0, saved_filename)  # Заполняем сохраненным именем

tk.Label(root, text="Введите слово:").grid(row=2, column=0, padx=5, pady=5)
word_entry = tk.Entry(root, width=30)
word_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2)
word_entry.insert(0, saved_word)  # Заполняем сохраненным словом

tk.Label(root, text="Количество повторений:").grid(row=3, column=0, padx=5, pady=5)
count_entry = tk.Entry(root, width=30)
count_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=2)
count_entry.insert(0, str(saved_count))  # Заполняем сохраненным количеством

# Полоса прогресса
progress = ttk.Progressbar(root, length=300)
progress.grid(row=4, column=0, columnspan=3, padx=5, pady=10)

# Метка с процентами
percent_label = tk.Label(root, text="0%")
percent_label.grid(row=5, column=0, columnspan=3)

# Кнопка создания файла
create_button = tk.Button(root, text="Создать файл", command=create_file)
create_button.grid(row=6, column=0, columnspan=3, pady=10)

# Кнопка "Автор"
author_button = tk.Button(root, text="Автор", command=open_author_page)
author_button.grid(row=7, column=0, columnspan=3, pady=10)

# Запуск основного цикла
root.mainloop()
