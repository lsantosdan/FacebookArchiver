import os
import csv
import shutil
import piexif
from datetime import datetime
import re
from mutagen.mp4 import MP4, MP4Cover
import platform
import subprocess

# Function to convert timestamp to the required format
def format_timestamp(timestamp):
    if timestamp == 'Timestamp not found':
        dt = datetime.now()
    else:
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%Y%m%d%H%M%S")

# Function to handle filename conflicts
def handle_filename_conflict(file_path):
    base_dir = os.path.dirname(file_path)
    base_name, ext = os.path.splitext(os.path.basename(file_path))
    # Extract the numerical part of the filename
    match = re.search(r"(\d+)$", base_name)
    if match:
        num_part = match.group(1)
        new_num_part = str(int(num_part) + 1)
        new_base_name = base_name[:match.start(1)] + new_num_part
    else:
        new_base_name = base_name + "1"
    new_name = new_base_name + ext
    new_file_path = os.path.join(base_dir, new_name)
    i = 1
    while os.path.exists(new_file_path):
        new_num_part = str(int(num_part) + i)
        new_base_name = base_name[:match.start(1)] + new_num_part
        new_name = new_base_name + ext
        new_file_path = os.path.join(base_dir, new_name)
        i += 1
    return new_file_path

# Function to update system metadata (date created and date modified)
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

# Function to process the files
def process_files():
    photos_count = 0
    videos_count = 0

    # Read the CSV file
    with open('photosvideos_metadata.csv', 'r', encoding="utf-8-sig") as csv_file: 
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row

        # Loop through each row in the CSV file
        for row in csv_reader:
            filename = row[1]
            timestamp = row[2]
            description = row[3]

            # Check if the file exists in the "temp" folder
            file_path = os.path.join('temp', filename)
            if os.path.isfile(file_path):
                # Check if it's an image file
                if file_path.lower().endswith(('.jpg', '.jpeg')):
                    # Check if it's already a JPEG file
                    try:
                        piexif.load(file_path)
                        is_jpeg = True
                    except piexif.InvalidImageDataError:
                        is_jpeg = False
                    if is_jpeg:
                        # Modify EXIF tags
                        exif_dict = piexif.load(file_path)
                        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = timestamp.encode()
                        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = timestamp.encode()
                        exif_dict['0th'][piexif.ImageIFD.ImageDescription] = description.encode()
                        exif_dict['Exif'][piexif.ExifIFD.UserComment] = description.encode()
                        exif_bytes = piexif.dump(exif_dict)
                        piexif.insert(exif_bytes, file_path)

                        print(f"Processed image: {file_path}")
                        photos_count += 1
                    else:
                        # Rename the file with a unique timestamp-based name
                        new_file_path = os.path.join('temp', format_timestamp(timestamp) + os.path.splitext(filename)[1])
                        new_file_path = handle_filename_conflict(new_file_path)
                        os.rename(file_path, new_file_path)
                        file_path = new_file_path  # Update file_path to the new filename
                        print(f"Renamed file: {file_path}")

                        # Update system metadata (date created and date modified)
                        update_system_metadata(file_path, timestamp)

                        photos_count += 1
 
                # Check if it's a video file
                elif file_path.lower().endswith(('.mp4', '.mov')):
                    try:
                        # Open the video file
                        video = MP4(file_path)

                        # Modify the video description
                        video['\xa9des'] = [description]

                        # Add timestamp to metadata
                        timestamp_obj = datetime.strptime(timestamp, "%d/%m/%Y %H:%M")
                        video['©day'] = [timestamp_obj.day]
                        video['©year'] = [timestamp_obj.year]
                        video['©creation_time'] = [timestamp]

                        # Save the modified metadata
                        video.save()

                        print(f"Processed video: {file_path}")
                        videos_count += 1
                    except:
                        # Rename the file with a unique timestamp-based name
                        new_file_path = os.path.join('temp', format_timestamp(timestamp) + os.path.splitext(filename)[1])
                        new_file_path = handle_filename_conflict(new_file_path)
                        os.rename(file_path, new_file_path)
                        file_path = new_file_path  # Update file_path to the new filename
                        print(f"Renamed file: {file_path}")

                        # Update system metadata (date created and date modified)
                        update_system_metadata(file_path, timestamp)

                        videos_count += 1     

                # Rename the file with a unique timestamp-based name
                new_file_path = os.path.join('temp', format_timestamp(timestamp) + os.path.splitext(filename)[1])
                new_file_path = handle_filename_conflict(new_file_path)
                os.rename(file_path, new_file_path)
                file_path = new_file_path  # Update file_path to the new filename
                print(f"Renamed file: {file_path}")

                # Update system metadata (date created and date modified)
                update_system_metadata(file_path, timestamp)

    # Print the total count of photos and videos processed
    print(f"Total photos processed: {photos_count}")
    print(f"Total videos processed: {videos_count}")

# Run the process_files function
process_files()
