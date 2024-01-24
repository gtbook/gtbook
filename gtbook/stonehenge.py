# AUTOGENERATED! DO NOT EDIT! File to edit: ../stonehenge.ipynb.

# %% auto 0
__all__ = ['URL', 'read_stonehenge_image', 'read_training_image', 'load_json', 'calculate_intrinsics', 'extract_extrinsics',
           'extract_camera_matrix', 'calculate_rays', 'create_rays', 'load_npz_from_url', 'download_rays']

# %% ../stonehenge.ipynb 3
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import requests
from PIL import Image

# %% ../stonehenge.ipynb 5
URL = "https://raw.githubusercontent.com/gtbook/robotics/main/stonehenge/"

# %% ../stonehenge.ipynb 6
def read_stonehenge_image(path:str, downsampling_factor:int=1):
    """
    Read image from the Stonehenge dataset, and return as a PIL image.

    Returns:
    PIL.Image: Image object representing the image at the specified index.
    """
    # Get stream of image data
    url = f"{URL}/{path}"
    response = requests.get(url, stream=True)
    response.raise_for_status()  # This will raise an error for bad responses

    # Read image from stream
    image = Image.open(response.raw)
    
    # Blend image onto white background
    if downsampling_factor > 1:
        image = image.resize((image.width // downsampling_factor, image.height // downsampling_factor))
    rgb_image = Image.new('RGB', image.size, (255, 255, 255))
    rgb_image.paste(image, mask=image.split()[3])  # 3 is the index of the alpha channel
    return rgb_image


# %% ../stonehenge.ipynb 7
def read_training_image(index:int, downsampling_factor:int=1):
    """Read image from the stonehenge dataset, and return as a PIL image."""
    return read_stonehenge_image(f"train/render{index}.png", downsampling_factor)


# %% ../stonehenge.ipynb 12
def load_json(path):
    """
    Load and parse a JSON file from a relative path.

    Returns:
    dict: Parsed JSON data as a Python dictionary.
    """
    url = f"{URL}/{path}"
    response = requests.get(url)
    response.raise_for_status()  # This will raise an error for bad responses
    return response.json()


# %% ../stonehenge.ipynb 15
def calculate_intrinsics(image_size: tuple, camera_angle_x: float) -> np.ndarray:
    """Calculate the intrinsic matrix given the image size and camera angle."""
    W, H = image_size
    f = W / (2 * np.tan(camera_angle_x/2))
    return np.array([[f, 0, W/2], [0, f, H/2], [0, 0, 1]])

def extract_extrinsics(camera_data: dict, index: int) -> np.ndarray:
    """Extract the extrinsic matrix from the given camera_data."""
    wTc = np.array(camera_data["frames"][index]["transform_matrix"]) # Make sure to use the index parameter
    t = wTc[:3, 3] # translation
    R = wTc[:3, :3] # rotation
    return np.hstack((R.T, -R.T @ t.reshape(-1, 1)))

def extract_camera_matrix(camera_data, index:int, image_size: tuple) -> np.ndarray:
    """Read the 3x4 camera matrix associated with a training image."""
    K = calculate_intrinsics(image_size, camera_data['camera_angle_x'])
    M = extract_extrinsics(camera_data, index)
    return K @ M

# %% ../stonehenge.ipynb 24
def calculate_rays(M: np.ndarray, image_size: tuple) -> tuple:
    """ Calculate a batch of rays associated with every pixel in a given image.
        When given size (W, H), returns two tensors of shape (H, W, 3) and (H, W, 3).
    """
    W, H = image_size
    A, a = M[:, :3], M[:, 3]
    inv_A = np.linalg.inv(A)

    # Compute origin and expand to all pixels.
    t = -inv_A @ a
    ones = np.ones((H, W))
    T = np.einsum('i,hw->hwi', t, ones) # creates (H,W,3) batch
    
    # Batch compute directions for all pixels.
    x, y = np.meshgrid(np.linspace(0.5, W-0.5, W), np.linspace(0.5, H-0.5, H), indexing='xy')
    p_ = np.stack([x, y, ones], axis=-1)
    P = - np.einsum('ij,hwj->hwi', inv_A, p_ - a) # batch matrix multiply

    norms = np.linalg.norm(P, axis=-1, keepdims=True)
    D = P / (norms + 1e-8)

    return T, D

# %% ../stonehenge.ipynb 34
def create_rays(camera_data, M = 199, downsampling_factor = 1):
    """Create rays for the training images.
    Args:
        camera_data: Dictionary containing the camera data.
        M: Number of training images to use.
        downsampling_factor: Downsampling factor to apply to the images.
    Returns:
        x_samples: Tensor of shape (M, H, W, 6) containing the origins and directions of the rays.
        y_samples: Tensor of shape (M, H, W, 3) containing the color data for each pixel.
    """
    W, H = read_training_image(0, downsampling_factor).size

    # Pre-allocate tensors
    x_samples = np.empty((M, H, W, 6), dtype=np.float32)
    y_samples = np.empty((M, H, W, 3), dtype=np.float32)

    for i in range(M):
        image = read_training_image(i, downsampling_factor)  # Get the i-th image

        M = extract_camera_matrix(camera_data, i, image.size)
        origins, directions = calculate_rays(M, image.size)
        origins = origins.astype(np.float32)
        directions = directions.astype(np.float32)

        # Combine data for x_samples
        x_samples[i] = np.concatenate((origins, directions), axis=-1)

        # Use the color data for y_samples
        y_samples[i] = np.array(image, dtype=np.float32)/255.0
    
    # Convert to float32 and return:
    return x_samples, y_samples

# %% ../stonehenge.ipynb 37
def load_npz_from_url(url):
    """
    Loads a .npz file from the given URL and returns the contained arrays as a tuple.

    Parameters:
    url (str): URL of the .npz file.

    Returns:
    tuple: A tuple containing the loaded numpy arrays, or None if the request fails.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        response.raise_for_status()

        # Open the content of the response as a file-like object
        file_like_object = BytesIO(response.content)

        # Load the .npz file and return the contained arrays
        with np.load(file_like_object) as data:
            return tuple(data[key] for key in data)
    
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

# %% ../stonehenge.ipynb 39
def download_rays(M=100, downsampling_factor=4):
    url = f'{URL}/training_rays-{M}-{downsampling_factor}.npz'
    return load_npz_from_url(url)
