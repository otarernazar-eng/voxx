"""
Camera Service for Webcam Handling and Frame Decoding
"""
from typing import Optional
import numpy as np
from PIL import Image

try:
    import cv2
    CV2_AVAILABLE = True
except Exception:
    CV2_AVAILABLE = False
    cv2 = None


class CameraService:
    @staticmethod
    def decode_streamlit_image(uploaded_file_or_cam) -> Optional[np.ndarray]:
        """Convert Streamlit camera_input or file_uploader into BGR image array."""
        if uploaded_file_or_cam is None:
            return None
        try:
            image = Image.open(uploaded_file_or_cam)
            image_np = np.array(image.convert("RGB"))
            if CV2_AVAILABLE and cv2 is not None:
                # Convert RGB to BGR for OpenCV processing
                return cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            # Fallback to RGB array if cv2 is not available
            return image_np
        except Exception:
            return None

    @staticmethod
    def bgr_to_rgb(cv_img: np.ndarray) -> np.ndarray:
        """Convert BGR image to RGB for displaying in Streamlit."""
        if CV2_AVAILABLE and cv2 is not None and cv_img is not None:
            try:
                return cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            except Exception:
                pass
        return cv_img
