import os
import sys
from PIL import Image, ExifTags
from datetime import datetime

date_keys = (
    'DateTimeOriginal', 'DateTime'
)

allowed_extensions = (
    '.jpg', '.jpeg'
)

def get_photo_date(photo_path):
    file_date = datetime.utcfromtimestamp(os.path.getmtime(photo_path))
    try:
        img = Image.open(photo_path)
        exif_data = img._getexif()
        if exif_data is None:
            return file_date
        exif_items = { ExifTags.TAGS[k]: v for k, v in exif_data.items() if k in ExifTags.TAGS }
        for date_key in date_keys:
            if date_key in exif_items:
                date_string = exif_items[date_key].split()[0]
                return datetime.strptime(date_string, '%Y:%m:%d')
    except Exception as e:
        print(f'Error reading {photo_path}: {e}')
    return file_date
    
def organize_photos_by_year(source_dir):
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith(allowed_extensions):
                photo_path = os.path.join(root, file)
                date = get_photo_date(photo_path)
                if date:
                    year_dir = os.path.join(source_dir, str(date.year))
                    os.makedirs(year_dir, exist_ok=True)
                    new_photo_path = os.path.join(year_dir, file)
                    #os.rename(photo_path, new_photo_path)
                    print(f"Moved {file} to {new_photo_path}")
                else:
                    print(f"Date not found for {file}, skipping...")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('No source directory provided')
        exit(1)
    source_dir = sys.argv[1]
    if not os.path.exists(source_dir):
        print(os.path.basename(source_dir) + ' does not exist')
        exit(1)

    organize_photos_by_year(source_dir)
