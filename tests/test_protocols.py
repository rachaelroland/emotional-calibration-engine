"""Tests for protocol system and interventions."""

import pytest
from unittest.mock import Mock, patch

from emotional_calibration_engine.core import CoreEmotion, EmotionalState
from emotional_calibration_engine.protocols import (
    ProtocolStep,
    ProtocolTrigger,
    BeingSeenProtocol,
    ProtocolManager
)


class TestProtocolStep:
    """Test protocol step structure."""
    
    def test_protocol_step_creation(self):
        """Test creating a protocol step."""
        step = ProtocolStep(
            name="test_step",
            description="Test description",
            prompts=["Prompt 1", "Prompt 2"],
            wait_for_response=True,
            min_duration_seconds=30
        )
        
        assert step.name == "test_step"
        assert len(step.prompts) == 2
        assert step.wait_for_response is True
        assert step.min_duration_seconds == 30


class TestBeingSeenProtocol:
    """Test Being Seen protocol implementation."""
    
    def test_protocol_initialization(self):
        """Test protocol initializes with correct steps."""
        protocol = BeingSeenProtocol()
        
        assert protocol.name == "being_seen"
        assert len(protocol.steps) == 5
        assert protocol.current_step == 0
        assert protocol.completed is False
    
    def test_should_activate_with_keywords(self):
        """Test activation based on invisibility keywords."""
        protocol = BeingSeenProtocol()
        
        state = EmotionalState(
            emotions={emotion: 0.5 for emotion in CoreEmotion},
            valence=0,
            arousal=0.5,
            dominance=0.5,
            timestamp=0
        )
        
        # Test with invisibility keywords
        context_with_keywords = {
            'text': "I feel like nobody sees the real me"
        }
        assert protocol.should_activate(state, context_with_keywords) is True
        
        # Test without keywords
        context_without_keywords = {
            'text': "I'm having a good day"
        }
        assert protocol.should_activate(state, context_without_keywords) is False
    
    def test_should_activate_with_emotional_pattern(self):
        """Test activation based on emotional patterns."""
        protocol = BeingSeenProtocol()
        
        # High sadness, low dominance should activate
        sad_state = EmotionalState(
            emotions={
                CoreEmotion.SADNESS: 0.8,
                **{e: 0.3 for e in CoreEmotion if e != CoreEmotion.SADNESS}
            },
            valence=-0.6,
            arousal=0.3,
            dominance=0.2,
            timestamp=0
        )
        
        assert protocol.should_activate(sad_state, {}) is True
        
        # Low sadness should not activate
        happy_state = EmotionalState(
            emotions={
                CoreEmotion.JOY: 0.8,
                CoreEmotion.SADNESS: 0.2,
                **{e: 0.5 for e in CoreEmotion if e not in [CoreEmotion.JOY, CoreEmotion.SADNESS]}
            },
            valence=0.7,
            arousal=0.6,
            dominance=0.7,
            timestamp=0
        )
        
        assert protocol.should_activate(happy_state, {}) is False
    
    def test_protocol_progression(self):
        """Test protocol advances through steps correctly."""
        protocol = BeingSeenProtocol()
        
        state = EmotionalState(
            emotions={emotion: 0.5 for emotion in CoreEmotion},
            valence=0,
            arousal=0.5,
            dominance=0.5,
            timestamp=0
        )
        
        # First response
        response1 = protocol.get_next_response("", state)
        assert protocol.current_step == 1
        assert response1 in protocol.steps[0].prompts
        
        # Second response with user input
        response2 = protocol.get_next_response("I've been pretending for so long", state)
        assert protocol.current_step == 2
        assert response2 in protocol.steps[1].prompts
    
    def test_protocol_completion(self):
        """Test protocol completes correctly."""
        protocol = BeingSeenProtocol()
        protocol.current_step = len(protocol.steps)
        
        state = EmotionalState(
            emotions={emotion: 0.5 for emotion in CoreEmotion},
            valence=0,
            arousal=0.5,
            dominance=0.5,
            timestamp=0
        )
        
        final_response = protocol.get_next_response("", state)
        assert protocol.completed is True
        assert "You were never too much" in final_response
    
    def test_protocol_reset(self):
        """Test protocol can be reset to initial state."""
        protocol = BeingSeenProtocol()
        protocol.current_step = 3
        protocol.completed = True
        
        protocol.reset()
        
        assert protocol.current_step == 0
        assert protocol.completed is False


class TestProtocolManager:
    """Test protocol management system."""
    
    def test_manager_initialization(self):
        """Test protocol manager initializes with built-in protocols."""
        manager = ProtocolManager()
        
        assert 'being_seen' in manager.protocols
        assert isinstance(manager.protocols['being_seen'], BeingSeenProtocol)
    
    def test_protocol_selection(self):
        """Test selecting appropriate protocol for emotional state."""
        manager = ProtocolManager()
        
        # State that should trigger being_seen protocol
        state = EmotionalState(
            emotions={
                CoreEmotion.SADNESS: 0.8,
                **{e: 0.3 for e in CoreEmotion if e != CoreEmotion.SADNESS}
            },
            valence=-0.6,
            arousal=0.3,
            dominance=0.2,
            timestamp=0
        )
        
        context = {'text': "I wish someone could see me"}
        
        selected = manager.select_protocol(state, context)
        assert selected is not None
        assert isinstance(selected, BeingSeenProtocol)
    
    def test_no_protocol_selection(self):
        """Test when no protocol should be selected."""
        manager = ProtocolManager()
        
        # Neutral state
        state = EmotionalState(
            emotions={emotion: 0.5 for emotion in CoreEmotion},
            valence=0,
            arousal=0.5,
            dominance=0.5,
            timestamp=0
        )
        
        context = {'text': "Everything is fine"}
        
        selected = manager.select_protocol(state, context)
        assert selected is None


@pytest.fixture
def sample_protocol():
    """Fixture providing a sample protocol."""
    return BeingSeenProtocol()


@pytest.fixture
def protocol_manager():
    """Fixture providing a protocol manager."""
    return ProtocolManager()