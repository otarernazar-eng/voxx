"""
Camera Service for Webcam Handling and Frame Decoding
"""
from typing import Optional
import cv2
import numpy as np
from PIL import Image


class CameraService:
    @staticmethod
    def decode_streamlit_image(uploaded_file_or_cam) -> Optional[np.ndarray]:
        """Convert Streamlit camera_input or file_uploader into OpenCV BGR image array."""
        if uploaded_file_or_cam is None:
            return None
        try:
            image = Image.open(uploaded_file_or_cam)
            image_np = np.array(image.convert("RGB"))
            # Convert RGB to BGR for OpenCV processing
            return cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        except Exception:
            return None

    @staticmethod
    def bgr_to_rgb(cv_img: np.ndarray) -> np.ndarray:
        """Convert BGR OpenCV image to RGB for displaying in Streamlit."""
        return cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
