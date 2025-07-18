# Development Guide

## Current Project Status

### ✅ Completed
- Core emotion model with 6 basic emotions
- Emotional state representation with valence/arousal/dominance
- Basic protocol framework
- Being Seen protocol implementation
- Test infrastructure
- Project structure and packaging

### 🚧 In Progress
- Additional protocols from docs/
- Emotion blending algorithms
- State persistence
- Safety mechanisms

### 📋 Next Priority Tasks
1. Implement emotion decay/temporal dynamics
2. Add remaining protocols
3. Create CLI interface
4. Build input processing pipeline

## Architecture Overview

### Core Components

```python
# Emotion State Flow
User Input → Input Processor → Emotional Assessment → State Update
                                        ↓
Protocol Selection ← Calibration Check ←┘
        ↓
Response Generation → User
```

### Key Classes

1. **EmotionalState**
   - Represents a point-in-time emotional configuration
   - Validates boundaries (0-1 for intensities)
   - Calculates distance from center (equilibrium)

2. **EmotionalTopology**
   - Tracks emotional states over time
   - Detects patterns and trajectories
   - Identifies stable vs chaotic emotional orbits

3. **CalibrationEngine**
   - Main orchestrator
   - Determines when calibration is needed
   - Manages protocol selection

4. **Protocol**
   - Abstract base for all protocols
   - Defines activation criteria
   - Manages step-by-step progression

## Design Decisions

### Why 6 Core Emotions?
Based on Ekman's universal emotions, provides coverage while maintaining simplicity. Can be extended with secondary emotions through blending.

### Why Dimensional Model (VAD)?
Valence-Arousal-Dominance provides continuous representation complementing discrete emotions, backed by extensive research.

### Why Protocol-Based?
- Structured approach prevents harm
- Allows for careful pacing
- Enables research validation
- Maintains therapeutic boundaries

## Testing Strategy

### Unit Tests
Test individual components in isolation:
```python
# Test emotion bounds
def test_emotion_validation():
    with pytest.raises(ValueError):
        EmotionalState(emotions={CoreEmotion.JOY: 1.5}, ...)
```

### Integration Tests
Test component interactions:
```python
# Test full calibration cycle
def test_calibration_flow():
    engine = CalibrationEngine()
    # ... full flow test
```

### Scenario Tests (To Implement)
Test realistic emotional journeys:
- Crisis intervention
- Gradual healing
- Emotional stuck points

## Adding New Features

### Adding a New Protocol

1. **Create Protocol Class**
```python
class YourProtocol(Protocol):
    def __init__(self):
        super().__init__(name="your_protocol", 
                        description="What it does")
        self._load_steps()
    
    def _load_steps(self):
        self.steps = [
            ProtocolStep(name="step1", ...),
            # More steps
        ]
    
    def should_activate(self, state, context):
        # Activation logic
        pass
    
    def get_next_response(self, user_input, state):
        # Response generation
        pass
```

2. **Add Tests**
```python
class TestYourProtocol:
    def test_activation(self):
        # Test when it activates
    
    def test_progression(self):
        # Test step progression
```

3. **Register in ProtocolManager**
```python
def _load_builtin_protocols(self):
    self.protocols['your_protocol'] = YourProtocol()
```

### Adding Emotion Features

1. **Extend EmotionalState**
```python
@property
def emotional_complexity(self) -> float:
    """Measure how many emotions are significantly active."""
    active = sum(1 for e in self.emotions.values() if e > 0.3)
    return active / len(self.emotions)
```

2. **Add to Topology Analysis**
```python
def detect_emotional_loops(self) -> List[Tuple[CoreEmotion, ...]]:
    """Detect repetitive emotional patterns."""
    # Implementation
```

## Performance Considerations

### Current Bottlenecks
- Text analysis (when implemented) will be slowest
- Large emotion history storage

### Optimization Strategies
- Cache computed properties
- Limit history window
- Use numpy for calculations
- Async for I/O operations

## Security & Privacy

### Data Handling
- No PII in logs
- Emotional data stays local
- Export requires explicit consent
- Anonymization built-in

### Safety Boundaries
- Max session duration
- Escalation thresholds
- Mandatory pauses
- Exit phrases

## Debugging Tips

### Common Issues

1. **Protocol Not Activating**
   - Check activation criteria
   - Verify emotional thresholds
   - Test context matching

2. **Test Failures**
   - Ensure emotion values in bounds
   - Check async operations
   - Verify state transitions

3. **Performance Issues**
   - Profile with cProfile
   - Check history size
   - Monitor memory usage

### Useful Debug Commands
```python
# Print emotional state
print(state.to_vector())

# Visualize topology
for s in topology.history[-5:]:
    print(f"{s.timestamp}: {s.emotions}")

# Check protocol state
print(f"Step: {protocol.current_step}/{len(protocol.steps)}")
```

## Future Considerations

### Scalability
- Database backend for persistence
- Distributed protocol processing
- Multi-user support

### Research Integration
- A/B testing framework
- Metrics collection
- Study protocol support

### Clinical Integration
- FHIR compliance
- Therapist dashboards
- Treatment planning

## Resources

### Internal Docs
- `/docs/` - Original protocol descriptions
- `/iteration_todos/` - Detailed task breakdowns
- `/tests/` - Examples of component usage

### External References
- Affective Computing papers
- Emotion regulation research
- Trauma-informed care guidelines
- Queer theory texts

## Questions for Discussion

When implementing new features, consider:

1. Does this respect user agency?
2. Could this cause emotional harm?
3. Is this culturally sensitive?
4. How do we validate effectiveness?
5. What are the privacy implications?

---

Remember: We're building a tool to help people understand themselves better. Every line of code should serve that purpose with care and respect.