import os
import csv
import shutil

def find_photo_video_files(directory, csv_file, temp_folder):
    photo_count = 0
    video_count = 0
    copied_files = set()
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        for root, dirs, files in os.walk(directory):
            # Exclude directories other than "posts" and "messages"
            if "posts" not in root and "messages" not in root:
                continue
            for filename in files:
                if not filename.lower().startswith('audioclip'):
                    file_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(file_path, directory).replace("\\", "/")
                    # Check if the file is a photo or video file based on its extension
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                        writer.writerow([relative_path])
                        photo_count += 1
                        # Copy the file to the temp folder if it hasn't been copied before
                        destination_path = os.path.join(temp_folder, filename).replace("\\", "/")
                        if destination_path not in copied_files:
                            shutil.copy(file_path, destination_path)
                            copied_files.add(destination_path)
                            print(f"Copied: {destination_path}")
                    elif filename.lower().endswith(('.mp4', '.avi', '.mov')):
                        writer.writerow([relative_path])
                        video_count += 1
                        # Copy the file to the temp folder if it hasn't been copied before
                        destination_path = os.path.join(temp_folder, filename).replace("\\", "/")
                        if destination_path not in copied_files:
                            shutil.copy(file_path, destination_path)
                            copied_files.add(destination_path)
                            print(f"Copied: {destination_path}")
    return photo_count, video_count

# Example usage:
directory_path = './'  # Replace with the directory path you want to search
csv_file_path = './photosvideos.csv'  # Replace with the desired CSV file path
temp_folder_path = os.path.join(directory_path, 'temp').replace("\\", "/")

# Create the temp folder if it doesn't exist
if not os.path.exists(temp_folder_path):
    os.makedirs(temp_folder_path)

# Create a new CSV file with a header
with open(csv_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Relative File Path'])

# Call the function to find photo and video files, append their relative paths to the CSV file, and copy them to the temp folder
photo_files, video_files = find_photo_video_files(directory_path, csv_file_path, temp_folder_path)
total_files = photo_files + video_files
print(f"Total files processed: {total_files}")
print(f"Photos found: {photo_files}")
print(f"Videos found: {video_files}")
print(f"Files copied to {temp_folder_path}")