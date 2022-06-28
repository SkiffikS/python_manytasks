# In this exercise, we will clean up the raw dataset.
import os
import glob
from PIL import Image
import numpy as np
import hashlib
import shutil
hash_function = hashlib.sha256()




def validate_images(input_dir, output_dir, log_file, formatter='06d'):
    number_of_valid_files = 0
    list_of_hashes = []
    failed_files = []
    input_dir = os.path.abspath(input_dir)
    # If output_dir or the directory containing log_file does not exist, your function should create them.

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    os.makedirs(os.path.dirname(log_file), exist_ok=True)






    image_files = sorted(glob.glob(os.path.join(input_dir, "**"), recursive=True))
    for image in image_files:
        # ditch all folders
        if not os.path.isdir(image):

            # ditch all file which are not .jpg, .JPG, .jpeg or .JPEG.
            if image.endswith('.jpg') or image.endswith('.JPG') or image.endswith('.jpeg') or image.endswith('.JPEG'):

                # ditch all files which are greater equal 250kB
                if os.path.getsize(image) <= 250000:

                    # ditch all "still not images"
                    try:
                        image_ = Image.open(image)


                        # ditch all with wrong shape etc
                        arr = np.array(image_)
                        if len(arr.shape) == 3 and arr.shape[0] >= 96 and arr.shape[1] >= 96 and arr.shape[2] == 3 and image_.mode == 'RGB':


                            # ditch all with varience = 0
                            if all(arr.std(axis=(0, 1)) > 0):


                                # ditch all which already appeared
                                arr_bytes = arr.tobytes()
                                hash_function = hashlib.sha256()
                                hash_function.update(arr_bytes)
                                hash_img = hash_function.digest()
                                if not hash_img in list_of_hashes:

                                    # Copy to out directory
                                    # os.rename(image)

                                    shutil.copy(image, os.path.join(output_dir, str(f"%{formatter}"%number_of_valid_files)+'.jpg'))
                                    number_of_valid_files += 1


                                # Collect all double images
                                else:
                                    failed_files.append([image,'6'])

                                # Update the list of hashes
                                list_of_hashes.append(hash_img)


                            # Var is zero ie. one color pic
                            else:
                                failed_files.append([image,'5'])

                        # Shape, Mode or size does not fit
                        else:
                            failed_files.append([image,'4'])


                    # collect images which could not be opened by PIL
                    except OSError:
                        failed_files.append([image,'3'])

                # The file size is greater 250kB (=250 000 Bytes)
                else:
                    failed_files.append([image,'2'])


            # The file name does NOT end with .jpg, .JPG, .jpeg or .JPEG.
            else:
                failed_files.append([image,'1'])

    # Write to logfile


    with open(log_file, "w") as f:
        # Extract the inputfile out of the imagepath
        for failed_file in failed_files:

            failed_file[0] = failed_file[0].split(os.path.sep)[len(input_dir.split(os.path.sep))::]
            failed_file[0] = os.path.join(*failed_file[0])
            s = ';'.join(failed_file)
            f.write(s + '\n')

    return number_of_valid_files








if __name__ == "__main__":
    print(validate_images('unittest\\unittest_input_9', 'output_dir', 'LOGS/log_file'))
    # print(validate_images('unittest', 'output_dir', 'LOGS/log_file'))