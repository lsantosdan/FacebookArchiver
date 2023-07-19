import os
import shutil

# Define the path to the "temp" folder
folder_path = 'temp'

# Get a list of all files in the "temp" folder
file_list = os.listdir(folder_path)

# Iterate over each file
for filename in file_list:
    # Extract the year, month, and extension from the filename
    year = filename[:4]
    month = filename[4:6]
    extension = filename[-4:]

    # Create the year and month folders if they don't already exist
    year_folder = os.path.join(folder_path, year)
    month_folder = os.path.join(year_folder, month)
    os.makedirs(month_folder, exist_ok=True)

    # Move the file to its respective year/month folder
    src_path = os.path.join(folder_path, filename)
    dest_path = os.path.join(month_folder, filename)
    shutil.move(src_path, dest_path)

print("Files have been successfully organized.")
