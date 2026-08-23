"""
Data model for Augmentative and Alternative Communication (AAC) phrases
"""
from dataclasses import dataclass


@dataclass
class AACPhrase:
    id: str
    text: str
    category: str
    icon: str
    bg_color: str = "#1A1A2E"
    is_emergency: bool = False
