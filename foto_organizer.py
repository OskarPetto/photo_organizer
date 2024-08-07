import os
import sys
from PIL import Image, ExifTags
from datetime import datetime

dateKeys = [
    'DateTimeOriginal', 'DateTime'
]

allowed_extensions = [
    '.jpg', '.jpeg', '.JPG', '.JPEG'
]

def readDate(file, img):
    if img is None:
        print(file + ' is no image')
        return None
    exif = img._getexif()
    if exif is None:
        exif = {}
    exif_items = { ExifTags.TAGS[k]: v for k, v in exif.items() if k in ExifTags.TAGS }
    for dateKey in dateKeys:
        if dateKey in exif_items:
            date_string = exif_items[dateKey].split()[0]
            return datetime.strptime(date_string, '%Y:%m:%d')
    return datetime.utcfromtimestamp(os.path.getmtime(file))

folder_name = sys.argv[1]
if not os.path.exists(folder_name):
    print(os.path.basename(folder_name) + ' does not exist')
    exit(1)

for file_name in os.listdir(folder_name):
    file_path = os.path.join(folder_name, file_name)
    if not os.path.isfile(file_path):
        continue
    _, file_extension = os.path.splitext(file_name)
    if file_extension not in allowed_extensions:
        continue
    img = Image.open(file_path)
    date = readDate(file_path, img)
    if date is not None:
        year = str(date.year)
        year_dir = os.path.join(folder_name, year)
        os.makedirs(year_dir, exist_ok=True)
        new_file_path = os.path.join(year_dir, file_name)
        os.rename(file_path, new_file_path)

