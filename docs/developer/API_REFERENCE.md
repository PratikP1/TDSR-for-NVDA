# TDSR for NVDA - API Reference

**Version:** 1.0.18
**Last Updated:** 2026-02-21

## Table of Contents

1. [Public Classes](#public-classes)
2. [Core Methods](#core-methods)
3. [Configuration API](#configuration-api)
4. [Extension API](#extension-api)
5. [Event Hooks](#event-hooks)

## Public Classes

### PositionCache

**Purpose**: Cache terminal position calculations to improve performance.

#### Methods

##### `get(bookmark) -> tuple[int, int] | None`

Retrieve cached position for a bookmark.

**Parameters**:
- `bookmark`: TextInfo bookmark object

**Returns**:
- `(row, col)` tuple if cache hit and valid
- `None` if cache miss or expired

**Example**:
```python
cache = PositionCache()
position = cache.get(textInfo.bookmark)
if position:
    row, col = position
```

##### `set(bookmark, row, col) -> None`

Store position in cache.

**Parameters**:
- `bookmark`: TextInfo bookmark object
- `row` (int): Row number (1-based)
- `col` (int): Column number (1-based)

**Example**:
```python
cache.set(textInfo.bookmark, 10, 25)
```

##### `clear() -> None`

Clear all cached positions.

**Example**:
```python
cache.clear()  # Clear on terminal switch
```

##### `invalidate(bookmark) -> None`

Invalidate a specific cached position.

**Parameters**:
- `bookmark`: TextInfo bookmark to invalidate

**Example**:
```python
cache.invalidate(textInfo.bookmark)
```

#### Constants

- `CACHE_TIMEOUT_MS` (int): Cache entry timeout in milliseconds (default: 1000)
- `MAX_CACHE_SIZE` (int): Maximum number of cached entries (default: 100)

---

### ANSIParser

**Purpose**: Parse ANSI escape sequences for color and formatting detection.

#### Methods

##### `__init__() -> None`

Initialize parser with default state.

**Example**:
```python
parser = ANSIParser()
```

##### `parse(text: str) -> dict`

Parse ANSI codes from text and return attributes.

**Parameters**:
- `text` (str): Text containing ANSI escape sequences

**Returns**:
Dictionary with keys:
- `foreground`: Color name, (R,G,B) tuple, or None
- `background`: Color name, (R,G,B) tuple, or None
- `bold` (bool): Text is bold
- `dim` (bool): Text is dim
- `italic` (bool): Text is italic
- `underline` (bool): Text is underlined
- `blink` (bool): Text is blinking
- `inverse` (bool): Colors are inverted
- `hidden` (bool): Text is hidden
- `strikethrough` (bool): Text has strikethrough

**Example**:
```python
parser = ANSIParser()
attrs = parser.parse('\x1b[31;1mRed Bold Text\x1b[0m')
print(attrs['foreground'])  # 'red'
print(attrs['bold'])  # True
```

##### `formatAttributes(mode='detailed') -> str`

Format current attributes as human-readable text.

**Parameters**:
- `mode` (str): Format mode - 'brief' or 'detailed'

**Returns**:
- Formatted attribute description string

**Example**:
```python
parser.parse('\x1b[31;1;4mText\x1b[0m')
description = parser.formatAttributes('detailed')
# Returns: "red foreground, bold, underline"
```

##### `reset() -> None`

Reset parser state to defaults.

**Example**:
```python
parser.reset()  # Clear all attributes
```

##### `stripANSI(text: str) -> str` (static)

Remove all ANSI escape sequences from text.

**Parameters**:
- `text` (str): Text with ANSI codes

**Returns**:
- Clean text without ANSI codes

**Example**:
```python
clean = ANSIParser.stripANSI('\x1b[31mRed\x1b[0m')
print(clean)  # 'Red'
```

#### Color Constants

- `STANDARD_COLORS` (dict): Standard color codes (30-37, 90-97)
- `BACKGROUND_COLORS` (dict): Background color codes (40-47, 100-107)
- `FORMAT_CODES` (dict): Format attribute codes (1-9)

---

### UnicodeWidthHelper

**Purpose**: Calculate display width for Unicode text (CJK, combining characters).

#### Methods (all static)

##### `getCharWidth(char: str) -> int`

Get display width of a single character.

**Parameters**:
- `char` (str): Single character

**Returns**:
- `0`: Combining character or control character
- `1`: Standard ASCII character
- `2`: CJK (Chinese/Japanese/Korean) character

**Example**:
```python
width = UnicodeWidthHelper.getCharWidth('A')  # 1
width = UnicodeWidthHelper.getCharWidth('中')  # 2
```

##### `getTextWidth(text: str) -> int`

Calculate total display width of text.

**Parameters**:
- `text` (str): Text string

**Returns**:
- Total display width in columns

**Example**:
```python
width = UnicodeWidthHelper.getTextWidth('Hello')  # 5
width = UnicodeWidthHelper.getTextWidth('你好')  # 4 (2+2)
```

##### `extractColumnRange(text: str, startCol: int, endCol: int) -> str`

Extract text from specific column range.

**Parameters**:
- `text` (str): Source text
- `startCol` (int): Starting column (1-based)
- `endCol` (int): Ending column (1-based, inclusive)

**Returns**:
- Text within specified column range

**Example**:
```python
text = 'Hello World'
result = UnicodeWidthHelper.extractColumnRange(text, 7, 11)
print(result)  # 'World'
```

##### `findColumnPosition(text: str, targetCol: int) -> int`

Find string index for a column position.

**Parameters**:
- `text` (str): Source text
- `targetCol` (int): Target column (1-based)

**Returns**:
- String index (0-based) corresponding to column

**Example**:
```python
text = 'Hello'
index = UnicodeWidthHelper.findColumnPosition(text, 3)
print(index)  # 2 (0-based index for column 3)
```

---

### WindowDefinition

**Purpose**: Define screen regions for window tracking.

#### Constructor

```python
WindowDefinition(name: str, top: int, bottom: int, left: int, right: int,
                 mode: str = 'announce', enabled: bool = True)
```

**Parameters**:
- `name` (str): Window name
- `top` (int): Top row (1-based)
- `bottom` (int): Bottom row (1-based)
- `left` (int): Left column (1-based)
- `right` (int): Right column (1-based)
- `mode` (str): Window mode - 'announce', 'silent', or 'monitor'
- `enabled` (bool): Whether window is active

**Example**:
```python
window = WindowDefinition('status', 1, 2, 1, 80, mode='silent')
```

#### Methods

##### `contains(row: int, col: int) -> bool`

Check if position is within window.

**Parameters**:
- `row` (int): Row number (1-based)
- `col` (int): Column number (1-based)

**Returns**:
- `True` if position is within window bounds
- `False` otherwise

**Example**:
```python
if window.contains(1, 40):
    print("Position is in window")
```

##### `toDict() -> dict`

Convert window to dictionary for serialization.

**Returns**:
- Dictionary with window properties

**Example**:
```python
data = window.toDict()
# {'name': 'status', 'top': 1, 'bottom': 2, ...}
```

##### `fromDict(data: dict) -> WindowDefinition` (class method)

Create window from dictionary.

**Parameters**:
- `data` (dict): Window properties

**Returns**:
- New WindowDefinition instance

**Example**:
```python
window = WindowDefinition.fromDict(data)
```

---

### ApplicationProfile

**Purpose**: Application-specific configuration profile.

#### Constructor

```python
ApplicationProfile(appName: str, displayName: str = None)
```

**Parameters**:
- `appName` (str): Application identifier
- `displayName` (str): Human-readable name (optional)

**Example**:
```python
profile = ApplicationProfile('vim', 'Vim/Neovim')
```

#### Properties

Settings overrides (None = use global setting):
- `punctuationLevel` (int | None)
- `cursorTrackingMode` (int | None)
- `keyEcho` (bool | None)
- `linePause` (bool | None)
- `repeatedSymbols` (bool | None)
- `repeatedSymbolsValues` (str | None)
- `cursorDelay` (int | None)
- `quietMode` (bool | None)

Collections:
- `windows` (list): WindowDefinition objects
- `customGestures` (dict): Custom gesture mappings

#### Methods

##### `addWindow(name: str, top: int, bottom: int, left: int, right: int, mode: str = 'announce') -> WindowDefinition`

Add window definition to profile.

**Parameters**:
- `name` (str): Window name
- `top` (int): Top row
- `bottom` (int): Bottom row
- `left` (int): Left column
- `right` (int): Right column
- `mode` (str): Window mode

**Returns**:
- Created WindowDefinition

**Example**:
```python
profile.addWindow('editor', 1, 20, 1, 80, mode='announce')
profile.addWindow('status', 21, 24, 1, 80, mode='silent')
```

##### `getWindowAtPosition(row: int, col: int) -> WindowDefinition | None`

Get window containing position.

**Parameters**:
- `row` (int): Row number
- `col` (int): Column number

**Returns**:
- WindowDefinition if position is in a window
- None otherwise

**Example**:
```python
window = profile.getWindowAtPosition(5, 40)
if window and window.mode == 'silent':
    # Don't announce in this region
    pass
```

##### `toDict() -> dict`

Serialize profile to dictionary.

##### `fromDict(data: dict) -> ApplicationProfile` (class method)

Deserialize profile from dictionary.

---

### ProfileManager

**Purpose**: Manage application profiles and detection.

#### Constructor

```python
ProfileManager()
```

Initializes with default profiles for vim, tmux, htop, less, git, nano, irssi.

**Example**:
```python
manager = ProfileManager()
```

#### Properties

- `profiles` (dict): App name → ApplicationProfile
- `activeProfile` (ApplicationProfile | None): Currently active profile

#### Methods

##### `detectApplication(focusObject) -> str`

Detect application from focus object.

**Parameters**:
- `focusObject`: NVDA focus object

**Returns**:
- Application name if detected
- 'default' if no match

**Example**:
```python
appName = manager.detectApplication(api.getFocusObject())
```

##### `getProfile(appName: str) -> ApplicationProfile | None`

Get profile for application.

**Parameters**:
- `appName` (str): Application name

**Returns**:
- ApplicationProfile if exists
- None otherwise

**Example**:
```python
profile = manager.getProfile('vim')
if profile:
    # Use profile settings
    pass
```

##### `setActiveProfile(appName: str) -> None`

Set currently active profile.

**Parameters**:
- `appName` (str): Application name

**Example**:
```python
manager.setActiveProfile('vim')
```

##### `addProfile(profile: ApplicationProfile) -> None`

Add or update profile.

**Parameters**:
- `profile`: ApplicationProfile to add

**Example**:
```python
custom = ApplicationProfile('myapp')
manager.addProfile(custom)
```

##### `removeProfile(appName: str) -> None`

Remove profile (except default profiles).

**Parameters**:
- `appName` (str): Application name

**Example**:
```python
manager.removeProfile('myapp')
```

##### `exportProfile(appName: str) -> dict | None`

Export profile to dictionary.

**Parameters**:
- `appName` (str): Application name

**Returns**:
- Profile dictionary or None

**Example**:
```python
data = manager.exportProfile('vim')
```

##### `importProfile(data: dict) -> ApplicationProfile`

Import profile from dictionary.

**Parameters**:
- `data` (dict): Profile data

**Returns**:
- Imported ApplicationProfile

**Example**:
```python
profile = manager.importProfile(data)
```

---

## Configuration API

### Config Spec

Access TDSR configuration through NVDA's config system:

```python
import config

# Read settings
cursor_tracking = config.conf["TDSR"]["cursorTracking"]
punct_level = config.conf["TDSR"]["punctuationLevel"]

# Write settings
config.conf["TDSR"]["cursorDelay"] = 50
```

### Configuration Keys

| Key | Type | Default | Range | Description |
|-----|------|---------|-------|-------------|
| `cursorTracking` | bool | True | - | Enable cursor tracking |
| `cursorTrackingMode` | int | 1 | 0-3 | Tracking mode (Off/Standard/Highlight/Window) |
| `keyEcho` | bool | True | - | Announce typed characters |
| `linePause` | bool | True | - | Pause at line endings |
| `punctuationLevel` | int | 2 | 0-3 | Punctuation verbosity |
| `repeatedSymbols` | bool | False | - | Condense repeated symbols |
| `repeatedSymbolsValues` | str | '-_=!' | - | Symbols to condense |
| `cursorDelay` | int | 20 | 0-1000 | Cursor tracking delay (ms) |
| `quietMode` | bool | False | - | Temporarily disable announcements |
| `windowTop` | int | 0 | 0-10000 | Window top row |
| `windowBottom` | int | 0 | 0-10000 | Window bottom row |
| `windowLeft` | int | 0 | 0-10000 | Window left column |
| `windowRight` | int | 0 | 0-10000 | Window right column |
| `windowEnabled` | bool | False | - | Enable window tracking |

### Validation Helpers

#### `_validateInteger(value, minValue, maxValue, default, fieldName) -> int`

Validate integer configuration value.

**Parameters**:
- `value`: Value to validate
- `minValue` (int): Minimum allowed
- `maxValue` (int): Maximum allowed
- `default` (int): Default if invalid
- `fieldName` (str): Field name for logging

**Returns**:
- Validated value or default

**Example**:
```python
delay = _validateInteger(value, 0, 1000, 20, "cursorDelay")
```

#### `_validateString(value, maxLength, default, fieldName) -> str`

Validate string configuration value.

**Parameters**:
- `value`: Value to validate
- `maxLength` (int): Maximum length
- `default` (str): Default if invalid
- `fieldName` (str): Field name for logging

**Returns**:
- Validated value (truncated if needed) or default

**Example**:
```python
symbols = _validateString(value, 50, "-_=!", "repeatedSymbolsValues")
```

#### `_validateSelectionSize(startRow, endRow, startCol, endCol) -> tuple[bool, str | None]`

Validate selection size against resource limits.

**Parameters**:
- `startRow` (int): Starting row
- `endRow` (int): Ending row
- `startCol` (int): Starting column
- `endCol` (int): Ending column

**Returns**:
- `(True, None)` if valid
- `(False, error_message)` if exceeds limits

**Example**:
```python
valid, error = _validateSelectionSize(1, 5000, 1, 100)
if not valid:
    ui.message(error)
```

---

## Extension API

### Adding Navigation Commands

Create custom navigation scripts:

```python
@script(
    description=_("Your command description"),
    gesture="kb:NVDA+alt+yourkey"
)
def script_yourCommand(self, gesture):
    """Your command implementation."""
    # Check if in terminal
    if not self.isTerminalApp():
        gesture.send()
        return

    try:
        # Get review position
        reviewPos = self._getReviewPosition()
        if reviewPos is None:
            ui.message(_("Unable to navigate"))
            return

        # Your navigation logic
        # ...

        # Announce result
        ui.message("Result")
    except Exception:
        ui.message(_("Navigation failed"))
```

### Custom Profile Creation

```python
# Create custom profile
profile = ApplicationProfile('myapp', 'My Application')

# Configure settings
profile.punctuationLevel = 2
profile.cursorTrackingMode = 1
profile.keyEcho = True

# Add window definitions
profile.addWindow('header', 1, 5, 1, 80, mode='announce')
profile.addWindow('footer', 20, 24, 1, 80, mode='silent')

# Register profile
self._profileManager.addProfile(profile)
```

### Custom ANSI Processing

```python
# Parse ANSI codes
parser = ANSIParser()
attrs = parser.parse(text)

# Check specific attributes
if attrs['bold'] and attrs['foreground'] == 'red':
    # Custom handling for bold red text
    pass

# Strip ANSI codes
clean_text = ANSIParser.stripANSI(text)
```

---

## Event Hooks

### Terminal Events

#### `event_gainFocus(obj, nextHandler)`

Called when terminal gains focus.

**Use Cases**:
- Detect terminal application
- Activate application profile
- Bind review cursor
- Clear position cache

#### `event_typedCharacter(obj, nextHandler, ch)`

Called when character is typed.

**Use Cases**:
- Key echo
- Symbol processing
- Repeated symbol detection

#### `event_caret(obj, nextHandler)`

Called when caret position changes.

**Use Cases**:
- Cursor tracking
- Position announcement
- Window tracking

### Script Hooks

All navigation scripts follow this pattern:

```python
@script(description=_("Description"), gesture="kb:gesture")
def script_name(self, gesture):
    if not self.isTerminalApp():
        gesture.send()
        return
    # Implementation
```

---

## Constants

### Cursor Tracking Modes

```python
CT_OFF = 0        # No tracking
CT_STANDARD = 1   # Announce character
CT_HIGHLIGHT = 2  # Track highlights
CT_WINDOW = 3     # Window tracking
```

### Punctuation Levels

```python
PUNCT_NONE = 0    # No punctuation
PUNCT_SOME = 1    # Basic (.,?!;:)
PUNCT_MOST = 2    # Most symbols
PUNCT_ALL = 3     # All symbols
```

### Resource Limits

```python
MAX_SELECTION_ROWS = 10000     # Max rows for selection
MAX_SELECTION_COLS = 1000      # Max columns for selection
MAX_WINDOW_DIMENSION = 10000   # Max window coordinate
MAX_REPEATED_SYMBOLS_LENGTH = 50  # Max repeated symbols string
```

---

## Error Handling

All public methods should handle errors gracefully:

```python
try:
    # Operation
    result = operation()
except (RuntimeError, AttributeError) as e:
    # Specific exceptions
    import logHandler
    logHandler.log.error(f"TDSR: Operation failed - {type(e).__name__}: {e}")
    ui.message(_("Specific error message"))
except Exception as e:
    # Generic fallback
    import logHandler
    logHandler.log.error(f"TDSR: Unexpected error - {type(e).__name__}: {e}")
    ui.message(_("Generic error message"))
```

---

## References

- [NVDA Developer Guide](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html)
- [TextInfo API](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#textInfos)
- [NVDA Config System](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#config)
- [Script Decorator](https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#baseObject.ScriptableObject.script)

---

**Document Maintained By**: TDSR Development Team
**Last Updated**: 2026-02-21
