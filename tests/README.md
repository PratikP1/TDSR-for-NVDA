# TDSR Test Suite

Automated tests for the TDSR for NVDA add-on.

## Overview

This directory contains comprehensive unit tests for TDSR functionality. The test suite covers:

- Input validation and security hardening (v1.0.16)
- Position caching system (v1.0.15)
- Configuration management
- Selection operations
- Terminal detection

## Quick Start

```bash
# Install dependencies
pip install -r requirements-dev.txt

# Run all tests
python run_tests.py

# Or use pytest directly
pytest tests/
```

## Test Files

- `conftest.py` - pytest configuration and fixtures
- `test_validation.py` - Input validation and resource limits
- `test_cache.py` - PositionCache functionality
- `test_config.py` - Configuration management
- `test_selection.py` - Selection operations and terminal detection

## Coverage

Current coverage targets:
- Overall: 70%+ ✅
- Validation: 100% ✅
- Cache: 95% ✅
- Config: 85% ✅
- Selection: 80% ✅

## CI/CD

Tests run automatically via GitHub Actions on every push and pull request.

See `TESTING_AUTOMATED.md` in the root directory for detailed documentation.
