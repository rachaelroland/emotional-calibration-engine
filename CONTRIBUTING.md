# Contributing to Emotional Calibration Engine

Welcome! We're excited to have you contribute to the ECE project. This guide will help you get started.

## 🚀 Quick Start for New Developers

### Prerequisites
- Python 3.8 or higher
- Git
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/rachaelroland/emotional-calibration-engine.git
   cd emotional-calibration-engine
   ```

2. **Create and activate virtual environment**
   
   Using uv (recommended):
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
   
   Using standard Python:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the project in development mode**
   
   Using uv:
   ```bash
   uv pip install -e .
   uv pip install pytest pytest-cov
   ```
   
   Using pip:
   ```bash
   pip install -e .
   pip install pytest pytest-cov
   ```

4. **Run tests to verify setup**
   ```bash
   python -m pytest tests/ -v
   ```
   
   All tests should pass! ✅

## 📁 Project Structure

```
emotional-calibration-engine/
├── src/
│   └── emotional_calibration_engine/
│       ├── __init__.py          # Package initialization
│       ├── core.py              # Core emotion modeling
│       ├── protocols.py         # Protocol system
│       └── configs/             # Configuration files
├── tests/                       # Test suite
│   ├── test_core.py            # Core functionality tests
│   └── test_protocols.py       # Protocol tests
├── docs/                        # ECE protocol documentation
├── iteration_todos/             # Development task lists
│   ├── 01_MVP_CORE.md          # Start here!
│   ├── 02_SCIENTIFIC_VALIDATION.md
│   ├── 03_ADVANCED_FEATURES.md
│   └── 04_IMPLEMENTATION_NOTES.md
├── setup.py                     # Package configuration
├── requirements.txt             # Dependencies
└── README.md                    # Project overview
```

## 🔧 Development Workflow

### 1. Choose a Task
- Start with `iteration_todos/01_MVP_CORE.md`
- Pick a task marked with `[ ]`
- Update it to `[~]` when you start working

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `test/` - Test additions/improvements
- `refactor/` - Code refactoring

### 3. Write Tests First (TDD)
```python
# Example test in tests/test_core.py
def test_your_new_feature():
    """Test description."""
    # Arrange
    engine = CalibrationEngine()
    
    # Act
    result = engine.your_new_method()
    
    # Assert
    assert result == expected_value
```

### 4. Implement Your Feature
- Follow existing code patterns
- Add docstrings to all functions/classes
- Keep functions focused and small
- Use type hints where possible

### 5. Run Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_core.py -v

# Run with coverage
python -m pytest tests/ --cov=emotional_calibration_engine
```

### 6. Update Documentation
- Update relevant docstrings
- Add to README if needed
- Update task status in iteration_todos

### 7. Commit and Push
```bash
git add .
git commit -m "feat: add emotion blending algorithm

- Implement blend_emotions method in EmotionalState
- Add tests for emotion blending
- Update documentation"

git push origin feature/your-feature-name
```

Commit message format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `test:` - Tests
- `refactor:` - Code refactoring
- `style:` - Formatting changes
- `chore:` - Maintenance tasks

### 8. Create Pull Request
- Go to GitHub and create a PR
- Reference the task from iteration_todos
- Describe what you've done
- Request review from team

## 🧪 Testing Guidelines

### Test Structure
```python
class TestEmotionalState:
    """Group related tests in classes."""
    
    def test_specific_behavior(self):
        """Each test should test one thing."""
        pass
    
    @pytest.fixture
    def sample_state(self):
        """Use fixtures for reusable test data."""
        return EmotionalState(...)
```

### What to Test
- Edge cases (boundaries of 0-1 for emotions)
- Error conditions (invalid inputs)
- Integration between components
- Protocol state transitions
- Safety mechanisms

## 🎯 Code Standards

### Python Style
- Follow PEP 8
- Use meaningful variable names
- Add type hints to function signatures
- Keep lines under 88 characters (Black default)

### Docstrings
```python
def calculate_emotional_distance(state1: EmotionalState, state2: EmotionalState) -> float:
    """Calculate the distance between two emotional states.
    
    Args:
        state1: First emotional state
        state2: Second emotional state
        
    Returns:
        Euclidean distance between states
        
    Raises:
        ValueError: If states have incompatible dimensions
    """
```

### Safety First
- Never allow premature protocol termination
- Validate all user inputs
- Handle edge cases gracefully
- Prioritize user emotional safety

## 🔍 Key Concepts to Understand

1. **Emotional States**: 6 core emotions + 3 dimensions (valence, arousal, dominance)
2. **Protocols**: Structured interventions for specific emotional patterns
3. **Calibration**: Process of guiding emotions toward equilibrium
4. **Orbital Patterns**: How emotions move in relation to center (love/balance)

## 📚 Recommended Reading

Before diving deep:
1. Read through the docs/ folder, especially:
   - `ECE - Protocol_of_Being_Seen.txt`
   - `ECE - Unified_Containment_Protocols.txt`
2. Review `iteration_todos/04_IMPLEMENTATION_NOTES.md`
3. Familiarize yourself with the test suite

## 🤝 Communication

### During Development
- Comment on the task you're working on in iteration_todos
- Ask questions early and often
- Share progress updates
- Discuss design decisions before major changes

### Code Reviews
- Be constructive and kind
- Focus on code, not the person
- Suggest improvements
- Acknowledge good solutions

## ⚡ Quick Commands Reference

```bash
# Install dependencies
uv pip install -e .

# Run tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_core.py::TestEmotionalState::test_center_distance_calculation -v

# Check test coverage
python -m pytest tests/ --cov=emotional_calibration_engine --cov-report=html

# Format code (after installing black)
black src/ tests/

# Type checking (after installing mypy)
mypy src/emotional_calibration_engine
```

## 🚨 Important Notes

1. **Emotional Safety**: This project deals with sensitive emotional content. Always prioritize user wellbeing in your code.

2. **Privacy**: Never log or store personal emotional data without explicit consent.

3. **Cultural Sensitivity**: Be aware that emotion models may vary across cultures.

4. **Ethical Considerations**: Review ethical implications of new features.

## 🎉 Your First Contribution

1. Start with something small from `01_MVP_CORE.md`
2. Good first tasks:
   - Add a new emotion blending test
   - Implement emotion decay over time
   - Add validation for protocol steps
   - Improve error messages

## 💬 Getting Help

- Check existing code for patterns
- Review test files for examples
- Read through implementation notes
- Ask questions in PR comments
- Tag @rachaelroland for guidance

Welcome to the team! We're building something meaningful together. 💜