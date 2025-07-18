"""Tests for core emotion modeling components."""

import pytest
import numpy as np
from datetime import datetime

from emotional_calibration_engine.core import (
    CoreEmotion,
    EmotionalState,
    EmotionalTopology,
    CalibrationEngine
)


class TestEmotionalState:
    """Test EmotionalState data structure and validation."""
    
    def test_valid_emotional_state_creation(self):
        """Test creating a valid emotional state."""
        emotions = {
            CoreEmotion.JOY: 0.8,
            CoreEmotion.SADNESS: 0.2,
            CoreEmotion.ANGER: 0.1,
            CoreEmotion.FEAR: 0.3,
            CoreEmotion.DISGUST: 0.0,
            CoreEmotion.SURPRISE: 0.4
        }
        
        state = EmotionalState(
            emotions=emotions,
            valence=0.6,
            arousal=0.7,
            dominance=0.5,
            timestamp=datetime.now().timestamp()
        )
        
        assert state.emotions == emotions
        assert state.valence == 0.6
        assert state.arousal == 0.7
        assert state.dominance == 0.5
    
    def test_emotion_intensity_validation(self):
        """Test that emotion intensities must be between 0 and 1."""
        with pytest.raises(ValueError, match="Emotion intensity must be between 0 and 1"):
            EmotionalState(
                emotions={CoreEmotion.JOY: 1.5},
                valence=0,
                arousal=0.5,
                dominance=0.5,
                timestamp=0
            )
    
    def test_valence_validation(self):
        """Test that valence must be between -1 and 1."""
        with pytest.raises(ValueError, match="Valence must be between -1 and 1"):
            EmotionalState(
                emotions={CoreEmotion.JOY: 0.5},
                valence=1.5,
                arousal=0.5,
                dominance=0.5,
                timestamp=0
            )
    
    def test_center_distance_calculation(self):
        """Test calculation of distance from emotional center."""
        # All emotions at 0.5 should have distance 0
        centered_state = EmotionalState(
            emotions={emotion: 0.5 for emotion in CoreEmotion},
            valence=0,
            arousal=0.5,
            dominance=0.5,
            timestamp=0
        )
        assert centered_state.center_distance == pytest.approx(0.0)
        
        # Extreme state should have larger distance
        extreme_state = EmotionalState(
            emotions={
                CoreEmotion.JOY: 1.0,
                CoreEmotion.SADNESS: 0.0,
                CoreEmotion.ANGER: 1.0,
                CoreEmotion.FEAR: 0.0,
                CoreEmotion.DISGUST: 1.0,
                CoreEmotion.SURPRISE: 0.0
            },
            valence=1.0,
            arousal=1.0,
            dominance=1.0,
            timestamp=0
        )
        assert extreme_state.center_distance > 0.5
    
    def test_to_vector_conversion(self):
        """Test conversion of emotional state to vector."""
        state = EmotionalState(
            emotions={emotion: 0.5 for emotion in CoreEmotion},
            valence=0.2,
            arousal=0.8,
            dominance=0.4,
            timestamp=0
        )
        
        vector = state.to_vector()
        assert len(vector) == 9  # 6 emotions + 3 dimensions
        assert vector[-3] == 0.2  # valence
        assert vector[-2] == 0.8  # arousal
        assert vector[-1] == 0.4  # dominance


class TestEmotionalTopology:
    """Test emotional topology tracking and analysis."""
    
    def test_add_state_updates_history(self):
        """Test that adding states updates history and current state."""
        topology = EmotionalTopology()
        state1 = EmotionalState(
            emotions={emotion: 0.5 for emotion in CoreEmotion},
            valence=0,
            arousal=0.5,
            dominance=0.5,
            timestamp=0
        )
        
        topology.add_state(state1)
        assert len(topology.history) == 1
        assert topology.current_state == state1
    
    def test_trajectory_calculation(self):
        """Test emotional trajectory calculation."""
        topology = EmotionalTopology()
        
        # Add states with increasing joy
        for i in range(6):
            state = EmotionalState(
                emotions={
                    CoreEmotion.JOY: 0.1 + i * 0.1,
                    **{e: 0.5 for e in CoreEmotion if e != CoreEmotion.JOY}
                },
                valence=i * 0.1,
                arousal=0.5,
                dominance=0.5,
                timestamp=i
            )
            topology.add_state(state)
        
        trajectory = topology.calculate_trajectory(window_size=5)
        assert trajectory is not None
        assert trajectory[0] > 0  # Joy should be increasing
    
    def test_orbital_pattern_detection(self):
        """Test detection of stable vs unstable emotional patterns."""
        topology = EmotionalTopology()
        
        # Create stable pattern for joy, unstable for anger
        for i in range(20):
            state = EmotionalState(
                emotions={
                    CoreEmotion.JOY: max(0, min(1, 0.7 + np.random.normal(0, 0.01))),  # Stable
                    CoreEmotion.ANGER: max(0, min(1, 0.5 + np.random.normal(0, 0.3))),  # Unstable
                    **{e: 0.5 for e in CoreEmotion if e not in [CoreEmotion.JOY, CoreEmotion.ANGER]}
                },
                valence=0,
                arousal=0.5,
                dominance=0.5,
                timestamp=i
            )
            topology.add_state(state)
        
        stability = topology.find_orbital_patterns()
        assert stability[CoreEmotion.JOY] > stability[CoreEmotion.ANGER]


class TestCalibrationEngine:
    """Test calibration engine functionality."""
    
    def test_engine_initialization(self):
        """Test engine initializes properly."""
        engine = CalibrationEngine()
        assert engine.topology is not None
        assert isinstance(engine.protocols, dict)
    
    def test_needs_calibration_detection(self):
        """Test detection of when calibration is needed."""
        engine = CalibrationEngine()
        
        # Add displaced state
        displaced_state = EmotionalState(
            emotions={
                CoreEmotion.SADNESS: 0.9,
                CoreEmotion.JOY: 0.1,
                **{e: 0.5 for e in CoreEmotion if e not in [CoreEmotion.SADNESS, CoreEmotion.JOY]}
            },
            valence=-0.8,
            arousal=0.3,
            dominance=0.2,
            timestamp=0,
            context="feeling invisible"
        )
        engine.topology.add_state(displaced_state)
        
        needs_cal, reasons = engine.needs_calibration()
        assert needs_cal is True
        # Check that at least one reason is present
        assert len(reasons) > 0
        # The being_seen_protocol should be triggered
        assert "being_seen_protocol" in reasons


@pytest.fixture
def sample_emotional_state():
    """Fixture providing a sample emotional state."""
    return EmotionalState(
        emotions={emotion: 0.5 for emotion in CoreEmotion},
        valence=0,
        arousal=0.5,
        dominance=0.5,
        timestamp=0
    )


@pytest.fixture
def calibration_engine():
    """Fixture providing a calibration engine instance."""
    return CalibrationEngine()