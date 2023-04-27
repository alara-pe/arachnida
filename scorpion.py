from PIL import Image
from PIL.ExifTags import TAGS
import sys

def display_exif_data(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()

    if exif_data:
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            print(f"{tag_name}: {value}")
    else:
        print(f"No se encontraron metadatos EXIF en {image_path}")

def main():
    if len(sys.argv) < 2:
        print("Uso: ./scorpion FILE1 [FILE2 ...]")
        sys.exit(1)

    for image_path in sys.argv[1:]:
        print(f"Metadatos de {image_path}:")
        display_exif_data(image_path)
        print()

if __name__ == "__main__":
    main()