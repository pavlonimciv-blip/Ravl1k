import tkinter as tk
from tkinter import filedialog
import os
import shutil

def main():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    # Вибір файлів
    file_paths = filedialog.askopenfilenames(title="Вибери файли для видалення")

    # Вибір папки, якщо файли не вибрали
    folder_path = filedialog.askdirectory(title="Вибери папку для видалення") if not file_paths else None

    # Якщо нічого не вибрали — вихід
    if not file_paths and not folder_path:
        print("Нічого не вибрано. Вихід...")
        return

    # Видалення файлів
    if file_paths:
        for path in file_paths:
            if os.path.exists(path):
                try:
                    os.remove(path)
                    print(f"Видалено файл: {path}")
                except Exception as e:
                    print(f"Помилка при видаленні файлу {path}: {e}")
            else:
                print(f"Файл не знайдено: {path}")

    # Видалення папки
    if folder_path:
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                print(f"Видалено папку: {folder_path}")
            except Exception as e:
                print(f"Помилка при видаленні папки {folder_path}: {e}")
        else:
            print(f"Папку не знайдено: {folder_path}")

if __name__ == "__main__":
    main()
