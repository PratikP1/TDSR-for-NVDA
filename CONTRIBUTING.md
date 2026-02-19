# Contributing to TDSR for NVDA

Thank you for your interest in contributing to TDSR for NVDA! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other contributors

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:

1. **Clear title** describing the issue
2. **Detailed description** of the problem
3. **Steps to reproduce** the issue
4. **Expected behavior** vs. actual behavior
5. **Environment information:**
   - Windows version (10 or 11)
   - NVDA version
   - Terminal application and version
   - TDSR add-on version

### Suggesting Enhancements

Feature requests are welcome! Please include:

1. **Clear description** of the feature
2. **Use case** explaining why it's needed
3. **Proposed implementation** (if you have ideas)
4. **Alternatives considered**

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch** from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following the coding standards
4. **Test your changes** thoroughly
5. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: brief description"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request** on GitHub

## Development Setup

### Prerequisites

- Python 3.7 or later
- NVDA screen reader (for testing)
- Git
- Text editor or IDE (VS Code recommended)

### Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/PratikP1/TDSR-for-NVDA.git
   cd TDSR-for-NVDA
   ```

2. The project structure:
   ```
   TDSR-for-NVDA/
   ├── addon/
   │   ├── globalPlugins/
   │   │   └── tdsr.py
   │   └── doc/
   │       └── en/
   │           └── readme.html
   ├── manifest.ini
   ├── buildVars.py
   └── build.py
   ```

3. Make your changes to the code

4. Build the add-on:
   ```bash
   python build.py
   ```

5. Install and test:
   - The build creates a `.nvda-addon` file
   - Install it in NVDA by opening the file
   - Test in a supported terminal application

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use 4 spaces for indentation (not tabs)
- Maximum line length: 100 characters
- Use descriptive variable and function names

### Documentation

- Add docstrings to all functions and classes
- Use clear and concise comments
- Update user guide if adding features
- Keep CHANGELOG.md updated

### Example Code Style

```python
def myFunction(param1, param2):
	"""
	Brief description of what the function does.
	
	Args:
		param1: Description of first parameter
		param2: Description of second parameter
		
	Returns:
		Description of return value
	"""
	# Implementation
	result = param1 + param2
	return result
```

## Testing

### Manual Testing Checklist

Before submitting a pull request, test:

- [ ] All keyboard shortcuts work correctly
- [ ] Settings save and load properly
- [ ] Help system opens correctly
- [ ] No errors in NVDA log
- [ ] Works in Windows Terminal
- [ ] Works in PowerShell
- [ ] Works in Command Prompt
- [ ] All speech output is clear and accurate

### Testing in NVDA

1. Enable NVDA's Python console for debugging:
   - NVDA menu > Tools > Python console

2. Check NVDA log for errors:
   - NVDA menu > Tools > View log

3. Test with different NVDA versions if possible

## Commit Messages

Write clear, descriptive commit messages:

**Good:**
```
Add word spelling feature

- Implement spell-out functionality for current word
- Add NVDA+Alt+K double-press gesture
- Update user guide with new command
```

**Bad:**
```
Fixed stuff
Update code
Changes
```

## Documentation

When adding features:

1. Update `addon/doc/en/readme.html`
2. Add entry to `CHANGELOG.md`
3. Update `README.md` if needed
4. Update `ROADMAP.md` for significant features

## License

By contributing, you agree that your contributions will be licensed under the GNU General Public License v3.0, the same license as the project.

## Questions?

- Check existing issues on GitHub
- Create a new issue for questions
- Reach out to maintainers

## Recognition

Contributors will be recognized in:
- CHANGELOG.md
- GitHub contributors page
- Project documentation

Thank you for contributing to make terminals more accessible!
