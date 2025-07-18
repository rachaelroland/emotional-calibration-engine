"""Emotional Calibration Engine - A framework for nuanced emotional understanding."""

from .core import (
    CoreEmotion,
    EmotionalState,
    EmotionalTopology,
    CalibrationEngine
)
from .protocols import (
    Protocol,
    ProtocolStep,
    ProtocolManager,
    BeingSeenProtocol
)

__version__ = "0.1.0"
__all__ = [
    "CoreEmotion",
    "EmotionalState", 
    "EmotionalTopology",
    "CalibrationEngine",
    "Protocol",
    "ProtocolStep",
    "ProtocolManager",
    "BeingSeenProtocol"
]


# Convenience function for quick setup
def create_engine():
    """Create a pre-configured ECE instance."""
    engine = CalibrationEngine()
    protocol_manager = ProtocolManager()
    return engine, protocol_manager