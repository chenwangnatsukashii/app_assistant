import io
from PIL import Image, ImageDraw

def load_image(image_path, target_size=(700, 1400)):
    """
    Load and resize an image from the specified path while maintaining aspect ratio.
    :param image_path: Path to the image file.
    :param target_size: Tuple of (width, height) for resizing
    :return: tuple of (bytes representation of the image, original size, scale factors) or (None, None, None) if error
    """
    try:
        # Open and get original size
        image = Image.open(image_path)
        orig_width, orig_height = image.size
        print(f"Original image size: {orig_width}x{orig_height}")

        if orig_width <= target_size[0] and orig_height <= target_size[1]:
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            image_bytes = buffered.getvalue()

            return image_bytes, (orig_width, orig_height), (1, 1, 0, 0)
        
        # Calculate aspect ratio
        aspect_ratio = orig_height / orig_width
        
        # Calculate new dimensions maintaining aspect ratio
        if aspect_ratio > 1:  # Tall image
            new_height = target_size[1]
            new_width = int(new_height / aspect_ratio)
        else:  # Wide image
            new_width = target_size[0]
            new_height = int(new_width * aspect_ratio)
            
        # Create new image with padding
        padded_image = Image.new('RGB', target_size, (255, 255, 255))
        
        # Resize image
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Calculate padding
        left = (target_size[0] - new_width) // 2
        top = (target_size[1] - new_height) // 2
        
        # Paste resized image onto padded background
        padded_image.paste(resized_image, (left, top))
        
        # Calculate scale factors considering padding
        width_scale = orig_width / new_width
        height_scale = orig_height / new_height
        
        # Store padding offsets with scale factors
        scale_info = (width_scale, height_scale, left, top)
        
        # Convert to bytes
        buffered = io.BytesIO()
        padded_image.save(buffered, format="PNG")
        image_bytes = buffered.getvalue()
        
        return image_bytes, (orig_width, orig_height), scale_info
    except Exception as e:
        print(f"Error loading image: {e}")
        return None, None, None

def draw_box(image_path, coordinates, output_path, scale_info=None):
    """
    Draw a red bounding box on the image at the specified coordinates and save it.
    
    :param image_path: Path to the input image file
    :param coordinates: List of [x1, y1, x2, y2] coordinates
    :param output_path: Path where the output image should be saved
    :param scale_info: Tuple of (width_scale, height_scale, pad_left, pad_top) to convert from model coordinates
    :return: True if successful, False otherwise
    """
    try:
        # Open the image
        image = Image.open(image_path)
        
        # Scale coordinates if scale info is provided
        if scale_info:
            width_scale, height_scale, pad_left, pad_top = scale_info
            # Remove padding and apply scale
            scaled_coordinates = [
                int((coordinates[0] - pad_left) * width_scale),   # x1
                int((coordinates[1] - pad_top) * height_scale),   # y1
                int((coordinates[2] - pad_left) * width_scale),   # x2
                int((coordinates[3] - pad_top) * height_scale)    # y2
            ]
        else:
            scaled_coordinates = coordinates
            
        # Create a drawing object
        draw = ImageDraw.Draw(image)
        
        # Draw the rectangle with red color (RGB: 255, 0, 0)
        # Line width of 3 pixels
        draw.rectangle(scaled_coordinates, outline=(255, 0, 0), width=3)
        
        # Save the image
        image.save(output_path)
        return True
    except Exception as e:
        print(f"Error drawing box on image: {e}")
        return False