import subprocess
import os
import sys

# Function to redirect print output to both terminal and a log file
def log_print(message):
    print(message)
    with open("log.txt", "a") as log_file:
        log_file.write(message + "\n")

def count_files_in_folder(folder):
    count = sum(len(files) for _, _, files in os.walk(folder))
    return count

scripts = [
    ("1jsonextractor.py", "JSON Extractor", ": copying all .json content from your archive into one file..."),
    ("2jsoncleaner.py", "JSON Cleaner", ": removing formatting and tagging errors in the main .json file..."),
    ("3filecompiler.py", "File Compiler", ": copying all photos and videos to temp folder, and creating photosvideos.csv database..."),
    ("4metadatafinder.py", "Metadata Finder", ": creating photosvideos_metadata.csv database and updating each file with timestamp/description..."),
    ("5metadatacleaner.py", "Metadata Cleaner", ": adding clean filename to metadata database, fixing encoding..."),
    ("6imageconverter.py", "Image Converter", ": converting all image files to .jpg, updating filepaths in both databases..."),
    ("7fileenhancer.py", "File Enhancer", ": adding metadata from database to file (exif for photos, QTFF for videos, system for both). Renaming files based on timestamp. This will take approximately one second per file. Be patient."),
    ("8taggedenhancer.py", "You're tagged!", ": Renaming, adding metadata and copying tagged photos to temp folder..."),
    ("9fileorganizer.py", "File Organizer", ": creating month/year folders, and moving files accordingly...")
]

log_print("============================\n|| FACEBOOK ARCHIVER v0.2 ||\n||        CC BY-NC        ||\n============================\nRepository: https://github.com/lsantosdan/FacebookArchiver\n\nMake sure you have the 9 scripts unpacked and at the root of your archive folder.\nIt is preferable to only keep the \"posts\", \"messages\", and \"tagged\" folders.\n")

# Count the number of files in the folders
posts_files = count_files_in_folder("posts")
messages_files = count_files_in_folder("messages")
tagged_files = count_files_in_folder("tagged")

# Calculate the total number of files and the approximate processing time in minutes
total_files = posts_files + messages_files + tagged_files
processing_time_minutes = total_files / 70

# Print the information about the number of files and processing time
log_print(f"There are around {total_files} files to be processed.")
log_print(f"The entire process should take approximately {processing_time_minutes} minutes.")

input("Press any key to continue...")

# Create a separate log file to store the messages from lower-level scripts
with open("log_lower_level.txt", "w") as log_lower_level_file:
    for script, title, description in scripts:
        # Print message before executing the script
        log_print(f"Executing {title}, {description}")

        # Execute the script and capture its output
        process = subprocess.Popen(["python", script], stdout=subprocess.PIPE, text=True)
        output, _ = process.communicate()

        # Print the captured output to the terminal and both log files
        if output:
            log_print(output)
            log_lower_level_file.write(output)

        # Wait for the script to finish
        process.wait()

        # Print message after executing the script
        log_print(f"{title} succesfully completed.\n")

try:
    os.rename("temp", "UPLOAD")
    log_print("The 'temp' folder has been renamed to 'UPLOAD'.")
except FileNotFoundError:
    log_print("Error: The 'temp' folder does not exist.")
except FileExistsError:
    log_print("Error: The 'UPLOAD' folder already exists. Please remove or rename it before running this step.")

# Append the messages from the lower-level scripts log to the main log file
with open("log_lower_level.txt", "r") as log_lower_level_file:
    log_print("\nMessages from lower-level scripts:\n")
    for line in log_lower_level_file:
        log_print(line.strip())

# Remove the temporary log file for lower-level scripts
os.remove("log_lower_level.txt")

log_print("Huzzah! Your Facebook archive has been succesfully cleaned, updated, and reorganized.\nThe final export is in the UPLOAD folder, and it's ready to be uploaded to other file storages such as a NAS.\nCheck log.txt for details.\n")

input("Press any key to exit...")
