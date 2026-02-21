# Running Tests for TDSR for NVDA

This document describes how to run the automated test suite for TDSR.

## Python Version Requirements

**TDSR is compatible with NVDA 2019.3 and later**, which corresponds to:
- **Minimum Python Version**: 3.7 (NVDA 2019.3)
- **Maximum Python Version**: 3.11 (latest tested)
- **Tested Versions**: 3.7, 3.8, 3.9, 3.10, 3.11

The test suite runs on all these Python versions via CI/CD to ensure compatibility.

## Quick Start

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
python run_tests.py

# Or use pytest directly
pytest tests/
```

## Test Suite Overview

The TDSR test suite includes:

### Unit Tests
- **test_validation.py**: Input validation and resource limit tests (40+ tests)
- **test_cache.py**: PositionCache functionality and thread safety (15+ tests)
- **test_config.py**: Configuration management and sanitization (20+ tests)
- **test_selection.py**: Selection operations and terminal detection (25+ tests)
- **test_integration.py**: Integration tests for core workflows (30+ tests)
- **test_performance.py**: Performance benchmarks and regression tests (20+ tests)

### Coverage Goal
- **Overall Target**: 70%+ code coverage
- **Core Methods**: 80%+ coverage
- **Configuration**: 70%+ coverage

## Running Tests

### Run All Tests
```bash
python run_tests.py
```

### Run Specific Test File
```bash
pytest tests/test_validation.py
```

### Run Specific Test Class
```bash
pytest tests/test_validation.py::TestValidationFunctions
```

### Run Specific Test Method
```bash
pytest tests/test_validation.py::TestValidationFunctions::test_validate_integer_valid_value
```

### Run with Verbose Output
```bash
pytest tests/ -v
```

### Run with Coverage Report
```bash
pytest tests/ --cov=addon/globalPlugins --cov-report=html
```

Then open `htmlcov/index.html` in a browser to view the coverage report.

## Test Structure

```
tests/
├── __init__.py           # Test package initialization
├── conftest.py          # pytest fixtures and configuration
├── test_validation.py   # Input validation tests
├── test_cache.py        # Position cache tests
├── test_config.py       # Configuration tests
└── test_selection.py    # Selection and detection tests
```

## Writing New Tests

### Test Naming Convention
- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

### Example Test

```python
import unittest
from unittest.mock import Mock

class TestMyFeature(unittest.TestCase):
    """Test my new feature."""

    def setUp(self):
        """Set up test fixtures."""
        from globalPlugins import tdsr
        self.tdsr = tdsr

    def test_my_feature(self):
        """Test that my feature works."""
        result = self.tdsr.my_function()
        self.assertEqual(result, expected_value)
```

### Using Fixtures

```python
def test_with_terminal(mock_terminal):
    """Test using the mock_terminal fixture."""
    # mock_terminal is automatically provided
    assert mock_terminal.appModule.appName == "windowsterminal"
```

## Continuous Integration

Tests run automatically on:
- Every push to main, develop, or claude/* branches
- Every pull request to main or develop

The CI pipeline:
1. Runs tests on Python 3.7-3.11
2. Checks code quality with flake8
3. Builds the add-on package
4. Uploads coverage to Codecov (Python 3.11 only)

### Viewing CI Results

Check the "Actions" tab on GitHub to see test results.

## Code Quality Checks

### Run flake8
```bash
flake8 addon/globalPlugins --max-line-length=120
```

### Check Coverage
```bash
pytest tests/ --cov=addon/globalPlugins --cov-report=term-missing
```

The build will fail if coverage drops below 70%.

## Troubleshooting

### Import Errors
If you see import errors, make sure the addon directory is in your Python path:
```python
import sys
sys.path.insert(0, 'addon')
```

### Mock Issues
NVDA modules are mocked in `conftest.py`. If you need additional mocks, add them there.

### Windows-Specific Tests
Some tests may behave differently on Windows vs Linux. The CI runs on Windows to ensure compatibility.

## Test Coverage Report

After running tests with coverage, view the HTML report:
```bash
# Generate coverage report
pytest tests/ --cov=addon/globalPlugins --cov-report=html

# Open in browser (Windows)
start htmlcov/index.html

# Open in browser (Linux/Mac)
open htmlcov/index.html
```

## Performance Tests

For performance testing of critical operations:

```python
import time

def test_position_calculation_performance():
    """Test position calculation is fast enough."""
    start = time.time()
    # Run operation
    result = calculate_position(...)
    elapsed = time.time() - start

    # Should complete in reasonable time
    assert elapsed < 0.1  # 100ms
```

## Contributing Tests

When contributing new features:
1. Write tests for new functionality
2. Ensure existing tests still pass
3. Maintain or improve code coverage
4. Follow existing test patterns

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [unittest documentation](https://docs.python.org/3/library/unittest.html)
- [Coverage.py documentation](https://coverage.readthedocs.io/)
