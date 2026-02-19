# Testing Guide for TDSR for NVDA

This document provides comprehensive testing procedures for the TDSR for NVDA add-on.

## Pre-Testing Setup

### Required Environment
- [ ] Windows 10 or Windows 11
- [ ] NVDA 2019.3 or later installed
- [ ] At least one supported terminal application
- [ ] TDSR add-on installed

### Supported Terminal Applications
- Windows Terminal
- PowerShell (5.x)
- PowerShell Core (7.x+)
- Command Prompt (cmd.exe)
- Console Host (conhost.exe)

## Test Categories

### 1. Installation Testing

#### Test 1.1: Fresh Installation
**Steps:**
1. Download TDSR-1.0.0.nvda-addon
2. Press Enter on the file
3. Confirm installation

**Expected Result:**
- Installation completes without errors
- NVDA prompts to restart
- After restart, add-on appears in Add-ons Manager

**Status:** [ ] Pass [ ] Fail

#### Test 1.2: Upgrade Installation
**Steps:**
1. Install version 1.0.0
2. Install version 1.0.0 again (simulating upgrade)

**Expected Result:**
- Installation replaces existing version
- Settings are preserved
- No errors occur

**Status:** [ ] Pass [ ] Fail

#### Test 1.3: Uninstallation
**Steps:**
1. Open Add-ons Manager
2. Select TDSR
3. Press Remove button
4. Restart NVDA

**Expected Result:**
- Add-on removed successfully
- No traces left in NVDA configuration
- No errors in NVDA log

**Status:** [ ] Pass [ ] Fail

---

### 2. Terminal Detection Testing

#### Test 2.1: Windows Terminal Detection
**Steps:**
1. Open Windows Terminal
2. Observe NVDA announcements

**Expected Result:**
- NVDA announces: "TDSR terminal support active. Press NVDA+shift+f1 for help."

**Status:** [ ] Pass [ ] Fail [ ] N/A (Terminal not available)

#### Test 2.2: PowerShell Detection
**Steps:**
1. Open PowerShell
2. Observe NVDA announcements

**Expected Result:**
- NVDA announces terminal support is active

**Status:** [ ] Pass [ ] Fail

#### Test 2.3: Command Prompt Detection
**Steps:**
1. Open Command Prompt
2. Observe NVDA announcements

**Expected Result:**
- NVDA announces terminal support is active

**Status:** [ ] Pass [ ] Fail

#### Test 2.4: Non-Terminal Application
**Steps:**
1. Switch to a non-terminal application (e.g., Notepad)
2. Try TDSR commands

**Expected Result:**
- TDSR commands do not activate
- Normal NVDA behavior continues

**Status:** [ ] Pass [ ] Fail

---

### 3. Navigation Commands Testing

#### Test 3.1: Line Navigation - Previous
**Steps:**
1. In a terminal with some output, press NVDA+Alt+U

**Expected Result:**
- NVDA reads the previous line

**Status:** [ ] Pass [ ] Fail

#### Test 3.2: Line Navigation - Current
**Steps:**
1. Press NVDA+Alt+I

**Expected Result:**
- NVDA reads the current line

**Status:** [ ] Pass [ ] Fail

#### Test 3.3: Line Navigation - Next
**Steps:**
1. Press NVDA+Alt+O

**Expected Result:**
- NVDA reads the next line

**Status:** [ ] Pass [ ] Fail

#### Test 3.4: Word Navigation - Previous
**Steps:**
1. Type some text, press NVDA+Alt+J

**Expected Result:**
- NVDA reads the previous word

**Status:** [ ] Pass [ ] Fail

#### Test 3.5: Word Navigation - Current
**Steps:**
1. Press NVDA+Alt+K

**Expected Result:**
- NVDA reads the current word

**Status:** [ ] Pass [ ] Fail

#### Test 3.6: Word Navigation - Next
**Steps:**
1. Press NVDA+Alt+L

**Expected Result:**
- NVDA reads the next word

**Status:** [ ] Pass [ ] Fail

#### Test 3.7: Word Spelling
**Steps:**
1. Position on a word
2. Press NVDA+Alt+K twice quickly

**Expected Result:**
- Word is spelled out character by character

**Status:** [ ] Pass [ ] Fail

#### Test 3.8: Character Navigation - Previous
**Steps:**
1. Press NVDA+Alt+M

**Expected Result:**
- NVDA reads the previous character

**Status:** [ ] Pass [ ] Fail

#### Test 3.9: Character Navigation - Current
**Steps:**
1. Press NVDA+Alt+Comma

**Expected Result:**
- NVDA reads the current character

**Status:** [ ] Pass [ ] Fail

#### Test 3.10: Character Navigation - Next
**Steps:**
1. Press NVDA+Alt+Period

**Expected Result:**
- NVDA reads the next character

**Status:** [ ] Pass [ ] Fail

#### Test 3.11: Phonetic Character Reading
**Steps:**
1. Position on character 'a'
2. Press NVDA+Alt+Comma twice quickly

**Expected Result:**
- NVDA says "alpha" (phonetic for 'a')

**Status:** [ ] Pass [ ] Fail

---

### 4. Help System Testing

#### Test 4.1: Help Shortcut
**Steps:**
1. In a terminal, press NVDA+Shift+F1

**Expected Result:**
- User guide (readme.html) opens in default browser

**Status:** [ ] Pass [ ] Fail

#### Test 4.2: Help Announcement
**Steps:**
1. Open a terminal for the first time after installation

**Expected Result:**
- NVDA announces help is available with NVDA+shift+f1

**Status:** [ ] Pass [ ] Fail

---

### 5. Settings Testing

#### Test 5.1: Settings Dialog Access
**Steps:**
1. In terminal, press NVDA+Alt+C
2. Or: NVDA menu > Preferences > Settings > Terminal Settings

**Expected Result:**
- Terminal Settings panel opens

**Status:** [ ] Pass [ ] Fail

#### Test 5.2: Cursor Tracking Toggle
**Steps:**
1. Open Terminal Settings
2. Toggle "Enable cursor tracking"
3. Click OK
4. Test cursor movements

**Expected Result:**
- Setting saves correctly
- Cursor tracking behavior changes accordingly

**Status:** [ ] Pass [ ] Fail

#### Test 5.3: Key Echo Toggle
**Steps:**
1. Open Terminal Settings
2. Toggle "Enable key echo"
3. Click OK
4. Type characters

**Expected Result:**
- Characters are/aren't announced based on setting

**Status:** [ ] Pass [ ] Fail

#### Test 5.4: Line Pause Toggle
**Steps:**
1. Open Terminal Settings
2. Toggle "Pause at newlines"
3. Click OK

**Expected Result:**
- Setting saves correctly

**Status:** [ ] Pass [ ] Fail

#### Test 5.5: Symbol Processing
**Steps:**
1. Open Terminal Settings
2. Enable "Process symbols"
3. Click OK
4. Navigate to a symbol (e.g., $)
5. Press NVDA+Alt+Comma

**Expected Result:**
- Symbol name is announced (e.g., "dollar")

**Status:** [ ] Pass [ ] Fail

#### Test 5.6: Repeated Symbols
**Steps:**
1. Open Terminal Settings
2. Enable "Condense repeated symbols"
3. Set repeated symbols to "-_=!"
4. Click OK

**Expected Result:**
- Setting saves correctly

**Status:** [ ] Pass [ ] Fail

#### Test 5.7: Cursor Delay
**Steps:**
1. Open Terminal Settings
2. Change cursor delay to 100ms
3. Click OK

**Expected Result:**
- Setting saves correctly
- Cursor announcements delayed appropriately

**Status:** [ ] Pass [ ] Fail

#### Test 5.8: Settings Persistence
**Steps:**
1. Change multiple settings
2. Click OK
3. Restart NVDA
4. Check settings

**Expected Result:**
- All settings persist after restart

**Status:** [ ] Pass [ ] Fail

---

### 6. Special Features Testing

#### Test 6.1: Quiet Mode Toggle
**Steps:**
1. Press NVDA+Alt+Q
2. Observe announcement

**Expected Result:**
- NVDA announces "Quiet mode on"
- Automatic announcements stop

**Status:** [ ] Pass [ ] Fail

#### Test 6.2: Quiet Mode Off
**Steps:**
1. With quiet mode on, press NVDA+Alt+Q again

**Expected Result:**
- NVDA announces "Quiet mode off"
- Automatic announcements resume

**Status:** [ ] Pass [ ] Fail

#### Test 6.3: Selection Start
**Steps:**
1. Press NVDA+Alt+R

**Expected Result:**
- NVDA announces "Selection started"

**Status:** [ ] Pass [ ] Fail

#### Test 6.4: Selection End
**Steps:**
1. With selection active, press NVDA+Alt+R again

**Expected Result:**
- NVDA announces "Selection ended"

**Status:** [ ] Pass [ ] Fail

#### Test 6.5: Copy Mode
**Steps:**
1. Press NVDA+Alt+V

**Expected Result:**
- NVDA announces copy mode instructions

**Status:** [ ] Pass [ ] Fail

---

### 7. Compatibility Testing

#### Test 7.1: Windows 10 Compatibility
**Steps:**
1. Test all basic features on Windows 10

**Expected Result:**
- All features work correctly

**Status:** [ ] Pass [ ] Fail [ ] N/A

#### Test 7.2: Windows 11 Compatibility
**Steps:**
1. Test all basic features on Windows 11

**Expected Result:**
- All features work correctly

**Status:** [ ] Pass [ ] Fail [ ] N/A

#### Test 7.3: NVDA 2019.3 Compatibility
**Steps:**
1. Install TDSR on NVDA 2019.3
2. Test basic features

**Expected Result:**
- Add-on installs and works correctly

**Status:** [ ] Pass [ ] Fail [ ] N/A

#### Test 7.4: Latest NVDA Compatibility
**Steps:**
1. Install TDSR on latest NVDA version
2. Test all features

**Expected Result:**
- All features work correctly

**Status:** [ ] Pass [ ] Fail

---

### 8. Error Handling Testing

#### Test 8.1: NVDA Log Clean
**Steps:**
1. Use TDSR normally
2. Check NVDA log (NVDA menu > Tools > View log)

**Expected Result:**
- No errors or warnings related to TDSR

**Status:** [ ] Pass [ ] Fail

#### Test 8.2: Invalid Gestures
**Steps:**
1. Try TDSR commands in non-terminal applications

**Expected Result:**
- Commands pass through to application
- No errors occur

**Status:** [ ] Pass [ ] Fail

#### Test 8.3: Missing Help File
**Steps:**
1. Rename readme.html temporarily
2. Press NVDA+Shift+F1

**Expected Result:**
- NVDA announces error message gracefully

**Status:** [ ] Pass [ ] Fail

---

### 9. Performance Testing

#### Test 9.1: Response Time
**Steps:**
1. Press various navigation commands
2. Measure response time

**Expected Result:**
- Commands respond within 100ms

**Status:** [ ] Pass [ ] Fail

#### Test 9.2: Long Terminal Session
**Steps:**
1. Keep terminal open for extended period
2. Generate lots of output
3. Use TDSR commands

**Expected Result:**
- No performance degradation
- Memory usage stays reasonable

**Status:** [ ] Pass [ ] Fail

#### Test 9.3: Rapid Command Execution
**Steps:**
1. Execute navigation commands rapidly

**Expected Result:**
- All commands register correctly
- No freezing or lag

**Status:** [ ] Pass [ ] Fail

---

### 10. Integration Testing

#### Test 10.1: Other Add-ons
**Steps:**
1. Install another NVDA add-on
2. Test both add-ons

**Expected Result:**
- No conflicts occur
- Both add-ons work normally

**Status:** [ ] Pass [ ] Fail [ ] N/A

#### Test 10.2: NVDA Speech Settings
**Steps:**
1. Change NVDA speech settings (rate, volume)
2. Use TDSR commands

**Expected Result:**
- TDSR respects NVDA speech settings

**Status:** [ ] Pass [ ] Fail

---

## Test Summary

**Date Tested:** _______________  
**Tester:** _______________  
**NVDA Version:** _______________  
**Windows Version:** _______________  
**TDSR Version:** _______________

**Total Tests:** _____  
**Passed:** _____  
**Failed:** _____  
**N/A:** _____

**Pass Rate:** _____%

## Issues Found

| Test # | Description | Severity | Status |
|--------|-------------|----------|---------|
|        |             |          |         |

## Notes

_Add any additional observations, comments, or recommendations here._

---

## Regression Testing Checklist

Use this checklist when testing after bug fixes or updates:

- [ ] All previously passing tests still pass
- [ ] Bug fix resolves the reported issue
- [ ] No new issues introduced
- [ ] Settings still work correctly
- [ ] Help system still accessible
- [ ] Performance unchanged or improved

---

**Testing Completed By:** _______________  
**Date:** _______________  
**Signature:** _______________
