import os
import imageio.v2 as iio
from PIL import Image
import csv

def is_image_file(file_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    ext = os.path.splitext(file_path)[1].lower()
    return ext in image_extensions

def convert_to_jpeg(image_path):
    try:
        image_format = os.path.splitext(image_path)[1][1:].upper()
        if image_format != 'JPEG' and is_image_file(image_path):
            new_image_path = os.path.splitext(image_path)[0] + '.jpg'
            image = iio.imread(image_path)

            if image_format == 'PNG' and image.shape[2] == 4:
                # Convert PNG image with RGBA color mode to RGB
                image = Image.fromarray(image)
                image = image.convert('RGB')

            iio.imwrite(new_image_path, image)
            os.remove(image_path)
            # Search for old filename in photosvideos.csv and replace with new filename
            csv_file = 'photosvideos_metadata.csv'
            old_filename = os.path.split(image_path)[1]
            new_filename = os.path.split(new_image_path)[1]

            with open(csv_file, 'r', encoding="utf-8-sig", newline='') as file:
                reader = csv.reader(file)
                lines = [line for line in reader]

            # Search for the old filename in each line of the CSV file and replace it with the new filename
            for line in lines:
                for i, item in enumerate(line):
                    if old_filename in item:
                        line[i] = item.replace(old_filename, new_filename)

            with open(csv_file, 'w', encoding="utf-8-sig", newline='') as file:
                writer = csv.writer(file)
                writer.writerows(lines)
            print(f"Converted {image_path} to JPEG format.")
    except Exception as e:
        print(f"Error converting {image_path}: {e}")

def convert_images_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            image_path = os.path.join(root, file)
            if os.path.isfile(image_path) and not image_path.lower().endswith('.jpg'):
                convert_to_jpeg(image_path)

# Path to the folder containing the images
folder_path = 'temp'

# Convert images in the folder
convert_images_in_folder(folder_path)
