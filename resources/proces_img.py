import os

from PIL import Image


def resize_and_rotate_images(input_folder, output_folder, target_size=640, rotations=[0, 90, 180, 270]):
    """
    Resize images to square and save rotated versions to the output folder.
    
    Args:
    - input_folder (str): Folder containing the original images.
    - output_folder (str): Folder where resized and rotated images will be saved.
    - target_size (int): Width and height of the resized images.
    - rotations (list of int): List of rotation angles.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            with Image.open(os.path.join(input_folder, filename)) as img:
                # Calculate new size keeping aspect ratio
                max_side = max(img.width, img.height)
                new_size = (max_side, max_side)

                # Create a new image with white background
                new_img = Image.new('RGB', new_size, (255, 255, 255))
                new_img.paste(img, ((max_side - img.width) // 2, (max_side - img.height) // 2))

                # Resize if larger than target size
                if max_side > target_size:
                    new_img = new_img.resize((target_size, target_size), Image.Resampling.LANCZOS)

                # Save rotated versions
                for angle in rotations:
                    rotated_img = new_img.rotate(angle, expand=True)
                    save_path = os.path.join(output_folder, f"{filename.split('.')[0]}_{angle}.{filename.split('.')[1]}")
                    rotated_img.save(save_path)

# Example usage
resize_and_rotate_images("E:\dev\qwantec-dev\Imagenes DNI\Chile\img\input", "E:\dev\qwantec-dev\Imagenes DNI\Chile\img\output")
