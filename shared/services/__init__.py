"""
VoxX Services Init
"""
from voxx.shared.services.tts_service import TTSService
from voxx.shared.services.stt_service import STTService
from voxx.shared.services.camera_service import CameraService
from voxx.shared.services.permissions import render_permission_explanation, render_webrtc_permission_error

__all__ = [
    "TTSService",
    "STTService",
    "CameraService",
    "render_permission_explanation",
    "render_webrtc_permission_error"
]
