from glob import glob
import hashlib as hs
from shutil import copy
import numpy as np
from os import path, makedirs
from PIL import Image


hash_func = hs.sha256() # Вказуємо функцію хешування файлів


def get_files(input_dir: str, output_dir: str, log_file: str): # Функція для получення усіх файлів у дерикторії

    input_dir = path.abspath(input_dir) # створюємо нормаліний повний шлях до файла на будь-якому комп'ютері, на будь-якій системі

    if not path.exists(output_dir): # Перевіряємо чи існує така папка, якщо ні виконуємо умову в тілі

        makedirs(output_dir) # створюємо каталог

    makedirs(path.dirname(log_file), exist_ok = True) # створюємо лог файл

    files = glob(path.join(input_dir, "**"), recursive = True) # шукаємо усі без виключення файли у заданій директорії та поміщаємо їх у список
    files = sorted(files) # сортуємо список із шляхами до файлів

    return files # повертаєємо список із шляїами до файлів


def write_to_log_file(log_file: str, number: int, file: str): # Функція для запису данниї у лог файл

    if not path.exists(log_file): # якщо файл не існує

        way = "w" # задаємо спосіб для створення та запису з нуля

    else: # якщо існує

        way = "a" # використовуємо спосіб який дописує дані у вже існуючий файл залишаючи попередні дані

    with open(log_file, way) as f: # відкриваємо лог файл потрібним спосібом

        f.write(str(path.basename(file)) + ";" + str(number) + "\n") # записуємо у лог файл ім'я файла та номер помилки в 1 стрічку


def validate_images(input_dir: str, output_dir: str, log_file: str, formatter = "06d"): # основна функція для роботи із файлами

    files = get_files(input_dir, output_dir, log_file) # получаємо список файлів у змінну
    hash_list = [] # створюємо списоку куди будемо додавати хеші файлів які пройшли повну перевірку
    valid_files = 0 # Кількість підходящих файлів

    for file in files: # Приходимось по кожному файлу із списку

        if file[-3:] == "jpg" or file[-3:] == "JPG" or file[-4:] == "jpeg" or file[-4:] == "JPEG": # Перевіряємо файл на потрібні розширення

            if path.getsize(file) <= 250000: # Перевіряємо чи розмір зображення менший за 250 000 кігабайт

                try: # Блок обходу помилок

                    with Image.open(file) as image: # Відкриваємо зображення через модуль Pillow
                        img = np.array(image) # Перетворюємо зображення у список із списками із чисел, де число відповідає за певний колір

                        if img.ndim == 3 and img.shape[0] >= 96 and img.shape[1] >= 96 and img.shape[2] == 3: # Перевіряємо файл на режим, форму, розмір

                            if all(img.std(axis=(0, 1)) > 0): # Перевірка на кольоровість картинки

                                img_bytes = img.tobytes() # Переводимо зображення у байти 
                                hash_func = hs.sha256() # Вказуємо функцію хешування файлів
                                hash_func.update(img_bytes) # Оновлюємо словник елементами з іншого об’єкта 
                                hash_img = hash_func.digest() # Повернення перероблених даних

                                if not hash_img in hash_list: # Перевіряємо чи данного хешу не має у списку із хешами

                                    copy(file, path.join(output_dir, str(f"%{formatter}"%valid_files)+'.jpg')) # Додаємо файл
                                    valid_files += 1 # Зараховуємо файл у змінну кількості підходящих зоражень

                                else:   
                                    # якщо хеш у списку повторюється записуємо у лог файл значення файлу і номер помилки 6
                                    write_to_log_file(log_file, 6, file)


                                hash_list.append(hash_img)

                            else:
                                # Якщо картинка не кольорова записуємо у лог файл значення файлу і номер помилки 5
                                write_to_log_file(log_file, 5, file)

                        else:
                            # Якщо файл не пройшов перевірку на форму, режим або розмір записуємо у лог файл значення файлу і номер помилки 4
                            write_to_log_file(log_file, 4, file)

                except:
                    # Якщо у середині блока сталась помилка ігноруємо її і записуємо у лог файл значення файлу і номер помилки 3
                    write_to_log_file(log_file, 3, file)

            else:
                # Якщо розмір файлу перевищує 250 000кб записуємо у лог файл значення файлу і номер помилки 2
                write_to_log_file(log_file, 2, file)

        else:
            # Якщо розширення файлу не підходить записуємо у лог файл значення файлу і номер помилки 1
            write_to_log_file(log_file, 1, file)

    # Повертаємо кількість підходящих файлів
    return valid_files


if __name__ == "__main__":

    valid_files = validate_images(r"unittest/unittest_input_9", r"output_dir", r"LOGS/log_file")
    print(valid_files)