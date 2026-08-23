"""
VoxX Services Init
"""
from shared.services.tts_service import TTSService
from shared.services.stt_service import STTService
from shared.services.camera_service import CameraService
from shared.services.permissions import render_permission_explanation, render_webrtc_permission_error

__all__ = [
    "TTSService",
    "STTService",
    "CameraService",
    "render_permission_explanation",
    "render_webrtc_permission_error"
]
