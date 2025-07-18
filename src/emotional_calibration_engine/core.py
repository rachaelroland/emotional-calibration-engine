"""Core emotion modeling and calibration system."""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
from enum import Enum


class CoreEmotion(Enum):
    """Six core emotions based on affective neuroscience research."""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    DISGUST = "disgust"
    SURPRISE = "surprise"


@dataclass
class EmotionalState:
    """Represents a multi-dimensional emotional state."""
    
    emotions: Dict[CoreEmotion, float]  # Intensity 0-1
    valence: float  # -1 (negative) to 1 (positive)
    arousal: float  # 0 (calm) to 1 (activated)
    dominance: float  # 0 (submissive) to 1 (dominant)
    timestamp: float
    context: Optional[str] = None
    
    def __post_init__(self):
        """Validate emotional state parameters."""
        for emotion, intensity in self.emotions.items():
            if not 0 <= intensity <= 1:
                raise ValueError(f"Emotion intensity must be between 0 and 1, got {intensity}")
        
        if not -1 <= self.valence <= 1:
            raise ValueError(f"Valence must be between -1 and 1, got {self.valence}")
        
        if not 0 <= self.arousal <= 1:
            raise ValueError(f"Arousal must be between 0 and 1, got {self.arousal}")
            
        if not 0 <= self.dominance <= 1:
            raise ValueError(f"Dominance must be between 0 and 1, got {self.dominance}")
    
    @property
    def center_distance(self) -> float:
        """Calculate distance from emotional center (love/equilibrium)."""
        emotion_vector = np.array(list(self.emotions.values()))
        center_vector = np.ones_like(emotion_vector) * 0.5
        return np.linalg.norm(emotion_vector - center_vector)
    
    def to_vector(self) -> np.ndarray:
        """Convert emotional state to vector representation."""
        return np.array([
            *list(self.emotions.values()),
            self.valence,
            self.arousal,
            self.dominance
        ])


class EmotionalTopology:
    """Models the dynamic topology of emotional states."""
    
    def __init__(self):
        self.history: List[EmotionalState] = []
        self.current_state: Optional[EmotionalState] = None
        
    def add_state(self, state: EmotionalState):
        """Add a new emotional state to the topology."""
        self.history.append(state)
        self.current_state = state
    
    def calculate_trajectory(self, window_size: int = 5) -> Optional[np.ndarray]:
        """Calculate the trajectory of emotional movement."""
        if len(self.history) < window_size:
            return None
            
        recent_states = self.history[-window_size:]
        vectors = [state.to_vector() for state in recent_states]
        
        # Calculate derivative (emotional velocity)
        trajectory = np.diff(vectors, axis=0)
        return np.mean(trajectory, axis=0)
    
    def find_orbital_patterns(self) -> Dict[CoreEmotion, float]:
        """Identify which emotions are in stable orbits vs chaotic patterns."""
        if len(self.history) < 10:
            return {}
            
        orbital_stability = {}
        
        for emotion in CoreEmotion:
            intensities = [state.emotions.get(emotion, 0) for state in self.history[-20:]]
            
            # Calculate variance as measure of stability
            variance = np.var(intensities)
            orbital_stability[emotion] = 1.0 - min(variance * 2, 1.0)
            
        return orbital_stability


class CalibrationEngine:
    """Main engine for emotional calibration."""
    
    def __init__(self):
        self.topology = EmotionalTopology()
        self.protocols: Dict[str, 'Protocol'] = {}
        
    def assess_current_state(self, input_data: Dict) -> EmotionalState:
        """Assess emotional state from various inputs."""
        # This would integrate NLP, voice analysis, etc.
        # For now, simplified implementation
        emotions = {emotion: 0.5 for emotion in CoreEmotion}
        
        return EmotionalState(
            emotions=emotions,
            valence=input_data.get('valence', 0),
            arousal=input_data.get('arousal', 0.5),
            dominance=input_data.get('dominance', 0.5),
            timestamp=input_data.get('timestamp', 0),
            context=input_data.get('context')
        )
    
    def needs_calibration(self) -> Tuple[bool, List[str]]:
        """Determine if calibration is needed and which protocols to use."""
        if not self.topology.current_state:
            return False, []
            
        reasons = []
        
        # Check center distance
        if self.topology.current_state.center_distance > 0.7:
            reasons.append("high_displacement")
            
        # Check orbital stability
        stability = self.topology.find_orbital_patterns()
        unstable_emotions = [e for e, s in stability.items() if s < 0.3]
        if unstable_emotions:
            reasons.append("orbital_instability")
            
        # Check for specific patterns
        if self.topology.current_state.emotions.get(CoreEmotion.SADNESS, 0) > 0.8:
            if self.topology.current_state.context and "invisible" in self.topology.current_state.context:
                reasons.append("being_seen_protocol")
                
        return len(reasons) > 0, reasons