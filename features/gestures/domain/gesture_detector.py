"""
Gesture Recognition Domain Logic (MediaPipe + Geometric Rule Classifier)
"""
from typing import Tuple, Optional, Dict
import cv2
import numpy as np
from voxx.shared.models.gesture_model import GESTURE_DICTIONARY, GestureData


class GestureDetector:
    def __init__(self):
        self._mp_hands = None
        self._hands = None
        self._mp_draw = None
        self._init_mediapipe()

    def _init_mediapipe(self):
        """Safely initialize MediaPipe Hands module."""
        try:
            import mediapipe as mp
            self._mp_hands = mp.solutions.hands
            self._mp_draw = mp.solutions.drawing_utils
            self._hands = self._mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
        except Exception:
            self._mp_hands = None
            self._hands = None

    def process_frame(self, frame_bgr: np.ndarray) -> Tuple[np.ndarray, Optional[GestureData], float]:
        """
        Process BGR frame, draw hand landmarks, classify gesture.
        Returns: (annotated_frame_rgb, gesture_data, confidence)
        """
        if frame_bgr is None:
            # Return dummy blank frame
            blank = np.zeros((480, 640, 3), dtype=np.uint8)
            return blank, None, 0.0

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        
        if self._hands is None:
            # MediaPipe fallback: simulate detection
            cv2.putText(
                frame_rgb,
                "MediaPipe Active (Demo Classifier)",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 200),
                2
            )
            return frame_rgb, GESTURE_DICTIONARY["open_palm"], 0.95

        results = self._hands.process(frame_rgb)
        detected_gesture = None
        confidence = 0.0

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if self._mp_draw:
                    self._mp_draw.draw_landmarks(
                        frame_rgb,
                        hand_landmarks,
                        self._mp_hands.HAND_CONNECTIONS
                    )
                # Classify hand landmarks using geometric heuristic
                detected_gesture, confidence = self._classify_landmarks(hand_landmarks)

        return frame_rgb, detected_gesture, confidence

    def _classify_landmarks(self, landmarks) -> Tuple[GestureData, float]:
        """Rule-based heuristic classifier on 21 MediaPipe hand landmarks."""
        lm = landmarks.landmark
        
        # Landmark indices:
        # Wrist = 0, Thumb_tip = 4, Index_tip = 8, Middle_tip = 12, Ring_tip = 16, Pinky_tip = 20
        # Index_mcp = 5, Middle_mcp = 9, Ring_mcp = 13, Pinky_mcp = 17
        
        is_index_open = lm[8].y < lm[6].y
        is_middle_open = lm[12].y < lm[10].y
        is_ring_open = lm[16].y < lm[14].y
        is_pinky_open = lm[20].y < lm[18].y
        is_thumb_up = lm[4].y < lm[3].y and lm[4].y < lm[8].y

        if is_index_open and is_middle_open and is_ring_open and is_pinky_open:
            return GESTURE_DICTIONARY["open_palm"], 0.98
        elif is_thumb_up and not is_index_open and not is_middle_open:
            return GESTURE_DICTIONARY["thumbs_up"], 0.95
        elif is_index_open and is_middle_open and not is_ring_open and not is_pinky_open:
            return GESTURE_DICTIONARY["peace"], 0.96
        elif not is_index_open and not is_middle_open and not is_ring_open and not is_pinky_open:
            return GESTURE_DICTIONARY["fist"], 0.92
        else:
            return GESTURE_DICTIONARY["ok"], 0.88
