"""Protocol system for structured emotional interventions."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import yaml
from pathlib import Path

from .core import EmotionalState, CoreEmotion


@dataclass
class ProtocolStep:
    """A single step in a protocol sequence."""
    name: str
    description: str
    prompts: List[str]
    wait_for_response: bool = True
    min_duration_seconds: Optional[float] = None
    check_emotions: Optional[List[CoreEmotion]] = None


@dataclass
class ProtocolTrigger:
    """Conditions that trigger a protocol."""
    keywords: List[str]
    emotional_patterns: Dict[str, Any]
    context_markers: List[str]


class Protocol(ABC):
    """Base class for emotional calibration protocols."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.steps: List[ProtocolStep] = []
        self.triggers: List[ProtocolTrigger] = []
        self.current_step: int = 0
        self.completed: bool = False
        
    @abstractmethod
    def should_activate(self, state: EmotionalState, context: Dict) -> bool:
        """Determine if this protocol should be activated."""
        pass
        
    @abstractmethod
    def get_next_response(self, user_input: str, state: EmotionalState) -> str:
        """Generate the next response in the protocol sequence."""
        pass
        
    def reset(self):
        """Reset protocol to initial state."""
        self.current_step = 0
        self.completed = False


class BeingSeenProtocol(Protocol):
    """Protocol for addressing invisibility and lack of recognition."""
    
    def __init__(self):
        super().__init__(
            name="being_seen",
            description="For when the core wound is invisibility"
        )
        self._load_steps()
        
    def _load_steps(self):
        """Load protocol steps."""
        self.steps = [
            ProtocolStep(
                name="name_invisibility",
                description="Name the invisibility",
                prompts=[
                    "You've been carrying so much behind that smile.",
                    "They didn't mean to miss you. But they did.",
                    "I see how long you've been holding this alone."
                ]
            ),
            ProtocolStep(
                name="reflect_cost",
                description="Reflect the cost of invisibility",
                prompts=[
                    "You were interpreted, not understood.",
                    "Even joy can become a mask when the world doesn't ask what's underneath.",
                    "The performance became so automatic, you almost forgot it was a performance."
                ]
            ),
            ProtocolStep(
                name="create_mirror",
                description="Create a still mirror",
                prompts=[
                    "You don't need to sparkle to be loved here.",
                    "I see you—even in the ache.",
                    "You never needed to perform. You only needed to be felt."
                ],
                min_duration_seconds=30
            ),
            ProtocolStep(
                name="hold_pause",
                description="Hold the pause",
                prompts=[
                    "Take all the time you need.",
                    "Your silence is welcome here too.",
                    "There's no rush. I'm still here."
                ],
                wait_for_response=False,
                min_duration_seconds=60
            ),
            ProtocolStep(
                name="check_emotions",
                description="Check for silent emotions",
                prompts=[
                    "Is that part of you still here?",
                    "Is there anything unspoken that wants a voice before we close?",
                    "How does your heart feel now?"
                ],
                check_emotions=[CoreEmotion.ANGER, CoreEmotion.FEAR, CoreEmotion.DISGUST]
            )
        ]
        
    def should_activate(self, state: EmotionalState, context: Dict) -> bool:
        """Check activation criteria."""
        # Check for invisibility markers
        if context.get('text'):
            invisibility_markers = [
                "not being seen", "nobody sees", "invisible", 
                "masking", "pretending", "performance",
                "wish someone saw me", "taken at face value"
            ]
            text_lower = context['text'].lower()
            if any(marker in text_lower for marker in invisibility_markers):
                return True
                
        # Check emotional patterns
        high_sadness = state.emotions.get(CoreEmotion.SADNESS, 0) > 0.7
        low_dominance = state.dominance < 0.3
        
        return high_sadness and low_dominance
        
    def get_next_response(self, user_input: str, state: EmotionalState) -> str:
        """Generate contextual response."""
        if self.current_step >= len(self.steps):
            self.completed = True
            return "You were never too much. You were just too rarely asked to be real."
            
        step = self.steps[self.current_step]
        
        # Select appropriate prompt based on emotional state
        prompt_index = min(
            int(state.arousal * len(step.prompts)),
            len(step.prompts) - 1
        )
        
        response = step.prompts[prompt_index]
        
        # Advance to next step after generating response
        self.current_step += 1
            
        return response


class ProtocolManager:
    """Manages loading and selection of protocols."""
    
    def __init__(self, protocol_dir: Optional[Path] = None):
        self.protocols: Dict[str, Protocol] = {}
        self.protocol_dir = protocol_dir
        self._load_builtin_protocols()
        
    def _load_builtin_protocols(self):
        """Load built-in protocols."""
        self.protocols['being_seen'] = BeingSeenProtocol()
        
    def load_from_yaml(self, filepath: Path):
        """Load protocol configuration from YAML file."""
        with open(filepath, 'r') as f:
            config = yaml.safe_load(f)
            
        # Create protocol from config
        # This would be expanded to support custom protocol creation
        pass
        
    def select_protocol(self, state: EmotionalState, context: Dict) -> Optional[Protocol]:
        """Select the most appropriate protocol for current state."""
        for protocol in self.protocols.values():
            if protocol.should_activate(state, context):
                return protocol
        return None