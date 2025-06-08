import io
from PIL import Image

def load_image(image_path):
    """
    Load an image from the specified path.
    
    :param image_path: Path to the image file.
    :return: bytes representation of the image, or None if an error occurs.
    """
    try:
        image = Image.open(image_path)
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        image_bytes = buffered.getvalue()
        return image_bytes
    except Exception as e:
        print(f"Error loading image: {e}")
        return None