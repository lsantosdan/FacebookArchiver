import os
import re
import shutil
import piexif
from datetime import datetime, timedelta
import platform
import subprocess

def update_system_metadata(file_path, timestamp):
    if platform.system() == 'Windows':
        cmd_create = 'powershell.exe', '-Command', 'Set-ItemProperty -Path "{}" -Name CreationTime -Value ([System.DateTime]::Parse("{}"))'.format(file_path, timestamp)
        cmd_modified = 'powershell.exe', '-Command', 'Set-ItemProperty -Path "{}" -Name LastWriteTime -Value ([System.DateTime]::Parse("{}"))'.format(file_path, timestamp)
        subprocess.run(cmd_create, shell=True)
        subprocess.run(cmd_modified, shell=True)
    else:
        timestamp_obj = datetime.strptime(timestamp, "%d/%m/%Y %H:%M")
        timestamp_unix = timestamp_obj.timestamp()
        os.utime(file_path, (timestamp_unix, timestamp_unix))

def clean_filename(filename):
    filename = filename.split("_", 1)[-1]
    filename = filename.replace("_", "")
    filename = filename[:14].ljust(14, '0')
    return filename

def rename_files_in_tagged_folder(folder_path):
    photos_count = 0

    if not os.path.exists(folder_path):
        print("The specified folder does not exist.")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        cleaned_filename = clean_filename(filename)

        timestamp_str = cleaned_filename[:14]
        try:
            timestamp = datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
        except ValueError:
            print(f"Invalid timestamp format in filename: {filename}")
            continue

        new_filename = cleaned_filename[:14]
        new_filename_with_extension = new_filename + os.path.splitext(filename)[-1]
        new_file_path = os.path.join(folder_path, new_filename_with_extension)

        i = 1
        while os.path.exists(new_file_path):
            timestamp += timedelta(seconds=1)
            new_filename = timestamp.strftime("%Y%m%d%H%M%S") + cleaned_filename[14:]
            new_filename_with_extension = new_filename + os.path.splitext(filename)[-1]
            new_file_path = os.path.join(folder_path, new_filename_with_extension)
            i += 1

        os.rename(file_path, new_file_path)
        print(f"Renamed: {filename} -> {os.path.basename(new_file_path)}")

        update_system_metadata(new_file_path, timestamp.strftime("%d/%m/%Y %H:%M"))

        if new_file_path.lower().endswith(('.jpg', '.jpeg')):
            try:
                piexif.load(new_file_path)
                is_jpeg = True
            except piexif.InvalidImageDataError:
                is_jpeg = False
            if is_jpeg:
                exif_dict = piexif.load(new_file_path)
                exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = timestamp.strftime("%Y:%m:%d %H:%M:%S").encode()
                exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = timestamp.strftime("%Y:%m:%d %H:%M:%S").encode()
                exif_bytes = piexif.dump(exif_dict)
                piexif.insert(exif_bytes, new_file_path)

                print(f"Processed image: {new_file_path}")
                photos_count += 1
            else:
                photos_count += 1
                print(f"Processed image: {new_file_path}")

    print(f"Total photos processed: {photos_count}")

def copy_files_to_temp_folder(folder_path):
    temp_folder_path = "temp"
    if not os.path.exists(temp_folder_path):
        os.mkdir(temp_folder_path)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        temp_file_path = os.path.join(temp_folder_path, filename)

        try:
            shutil.copy2(file_path, temp_file_path)
            print(f"Copied: {filename} -> {os.path.basename(temp_file_path)}")
        except Exception as e:
            print(f"Error copying {filename}: {str(e)}")

if __name__ == "__main__":
    folder_path = "tagged"  # Replace this with the actual path to the "tagged" folder

    if not os.path.exists(folder_path):
        print("The specified folder does not exist.")
    else:
        rename_files_in_tagged_folder(folder_path)
        copy_files_to_temp_folder(folder_path)
