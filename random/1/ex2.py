import glob
import hashlib
import os
import shutil

import PIL
import numpy as np
from PIL import ImageStat

def check_files(input_dir: str, hash_table: list, output_dir: str, log_file: str, formatter: str = None) -> None:
    # Search for files in the input directory
    image_files = sorted(glob.glob(os.path.join(input_dir, "*")))
    for i in image_files:
        if os.path.isdir(i):
            check_files(i, hash_table, output_dir, log_file, formatter)
        else:
            hash_table = is_valid(i, hash_table, output_dir, log_file, formatter)

def write_log(log_file: str, nr: int, file: str) -> None:
    if not os.path.exists(log_file):
        m = 'w'
    else:
        m = 'a'
    with open(log_file, m) as f:
        f.write(f'{os.path.basename(file)};{nr}\n')


def is_valid(file: str, hash_table: list, output_dir: str, log_file: str, formatter: str = None) -> list:

    # Check whether the file is a jpg file
    if os.path.basename(file).split('.')[-1] not in ['jpg', 'JPG', 'jpeg', 'JPEG']:
        write_log(log_file, 1, file)
        return hash_table

    # Check whether the size of the file is greater than 250000 bytes
    if os.path.getsize(file) > 250000:
        write_log(log_file, 2, file)
        return hash_table

    # Check whether the file is a valid image (PIL does not rise exception)
    try:
        with PIL.Image.open(file) as im:
            image = np.array(im)

            if image.ndim != 3:
                write_log(log_file, 4, file)
                return hash_table

            if image.shape[0] < 96 or image.shape[1] < 96 or image.shape[2] != 3:
                write_log(log_file, 4, file)
                return hash_table

            if im.mode != 'RGB':
                write_log(log_file, 3, file)
                return hash_table

            stat = ImageStat.Stat(im)

            if sum(stat.var) == 0:
                write_log(log_file, 5, file)
                return hash_table
    except:
        write_log(log_file, 3, file)
        return hash_table

    np_image_bytes = image.tostring()
    hashing_function = hashlib.sha256()
    hashing_function.update(np_image_bytes)
    np_image_hash = hashing_function.digest()

    if np_image_hash in hash_table:
        write_log(log_file, 6, file)
        return hash_table
    else:

        formatter = int(formatter[0:2])
        name = str(len(hash_table)).zfill(formatter)
        shutil.copy(file, os.path.join(output_dir, f'{name}.jpg'))
        hash_table.append(np_image_hash)
        return hash_table


def validate_images(input_dir: str, output_dir: str, log_file: str, formatter: str = None) -> int:
    input_dir = os.path.abspath(input_dir)

    hash_table = []

    # Check whether input directory exists or not
    if not os.path.exists(output_dir):
        # Create a new directory because it does not exist
        os.makedirs(output_dir)

    log_file_ = log_file.split('/')[-1]
    directory_log = log_file.replace(log_file_, '')

    # Check whether the directory where the log file should be exists or not
    if not os.path.exists(directory_log):
        # Create a new directory because it does not exist
        os.makedirs(directory_log)

    # Search for files in the input directory
    check_files(input_dir, hash_table, output_dir, log_file, formatter)
    return len(hash_table)
