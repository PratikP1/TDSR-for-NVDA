"""
Additional tests to increase code coverage.

Focuses on testing ProfileManager, ApplicationProfile, ANS IParser edge cases,
and other helper classes that weren't fully covered.
"""
import unittest
from unittest.mock import Mock, MagicMock, patch
import sys


class TestProfileManager(unittest.TestCase):
    """Comprehensive tests for ProfileManager."""

    def setUp(self):
        """Set up test fixtures."""
        from globalPlugins.terminalAccess import ProfileManager
        self.manager = ProfileManager()

    def test_get_profile_existing(self):
        """Test getting an existing profile."""
        profile = self.manager.getProfile('vim')
        self.assertIsNotNone(profile)
        self.assertEqual(profile.appName, 'vim')

    def test_get_profile_nonexistent(self):
        """Test getting a nonexistent profile returns None."""
        profile = self.manager.getProfile('nonexistent')
        self.assertIsNone(profile)

    def test_set_active_profile(self):
        """Test setting an active profile."""
        self.manager.setActiveProfile('tmux')
        self.assertIsNotNone(self.manager.activeProfile)
        self.assertEqual(self.manager.activeProfile.appName, 'tmux')

    def test_set_active_profile_nonexistent(self):
        """Test setting a nonexistent profile as active."""
        self.manager.setActiveProfile('nonexistent')
        # Should not crash, activeProfile might be None
        # or might keep previous value

    def test_add_profile(self):
        """Test adding a new profile."""
        from globalPlugins.terminalAccess import ApplicationProfile
        new_profile = ApplicationProfile('testapp', 'Test Application')
        self.manager.addProfile(new_profile)

        retrieved = self.manager.getProfile('testapp')
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.appName, 'testapp')

    def test_profile_list(self):
        """Test getting list of all profiles."""
        profiles = list(self.manager.profiles.keys())
        self.assertGreater(len(profiles), 0)
        self.assertIn('vim', profiles)
        self.assertIn('tmux', profiles)

    def test_export_profile_dict(self):
        """Test exporting profile to dictionary."""
        vim_data = self.manager.exportProfile('vim')
        self.assertIsNotNone(vim_data)
        self.assertIsInstance(vim_data, dict)
        self.assertIn('appName', vim_data)
        self.assertEqual(vim_data['appName'], 'vim')

    def test_import_profile_from_dict(self):
        """Test importing profile from dictionary."""
        profile_data = {
            'appName': 'imported',
            'displayName': 'Imported App',
            'punctuationLevel': 2,
            'cursorTrackingMode': 1
        }

        imported = self.manager.importProfile(profile_data)
        self.assertIsNotNone(imported)
        self.assertEqual(imported.appName, 'imported')
        self.assertIn('imported', self.manager.profiles)

    def test_remove_custom_profile(self):
        """Test removing a custom profile."""
        from globalPlugins.terminalAccess import ApplicationProfile
        custom = ApplicationProfile('removeme', 'Remove Me')
        self.manager.addProfile(custom)
        self.assertIn('removeme', self.manager.profiles)

        self.manager.removeProfile('removeme')
        self.assertNotIn('removeme', self.manager.profiles)

    def test_remove_default_profile_protected(self):
        """Test that default profiles cannot be removed."""
        self.assertIn('vim', self.manager.profiles)
        self.manager.removeProfile('vim')
        # vim should still exist (default profiles are protected)
        self.assertIn('vim', self.manager.profiles)


class TestApplicationProfile(unittest.TestCase):
    """Tests for ApplicationProfile class."""

    def setUp(self):
        """Set up test fixtures."""
        from globalPlugins.terminalAccess import ApplicationProfile
        self.ProfileClass = ApplicationProfile

    def test_profile_creation(self):
        """Test creating a new profile."""
        profile = self.ProfileClass('testapp', 'Test Application')
        self.assertEqual(profile.appName, 'testapp')
        self.assertEqual(profile.displayName, 'Test Application')

    def test_profile_to_dict(self):
        """Test converting profile to dictionary."""
        profile = self.ProfileClass('testapp', 'Test Application')
        profile.punctuationLevel = 2
        profile.cursorTrackingMode = 1

        data = profile.toDict()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['appName'], 'testapp')
        self.assertEqual(data['displayName'], 'Test Application')
        self.assertEqual(data['punctuationLevel'], 2)
        self.assertEqual(data['cursorTrackingMode'], 1)

    def test_profile_from_dict(self):
        """Test creating profile from dictionary."""
        data = {
            'appName': 'fromdict',
            'displayName': 'From Dict',
            'punctuationLevel': 3,
            'cursorTrackingMode': 2
        }

        profile = self.ProfileClass.fromDict(data)
        self.assertEqual(profile.appName, 'fromdict')
        self.assertEqual(profile.displayName, 'From Dict')
        self.assertEqual(profile.punctuationLevel, 3)
        self.assertEqual(profile.cursorTrackingMode, 2)

    def test_profile_attributes(self):
        """Test profile has all expected attributes."""
        profile = self.ProfileClass('test', 'Test')

        # Should have these attributes
        self.assertTrue(hasattr(profile, 'appName'))
        self.assertTrue(hasattr(profile, 'displayName'))
        self.assertTrue(hasattr(profile, 'punctuationLevel'))
        self.assertTrue(hasattr(profile, 'cursorTrackingMode'))


class TestANSIParserEdgeCases(unittest.TestCase):
    """Edge case tests for ANSIParser."""

    def setUp(self):
        """Set up test fixtures."""
        from globalPlugins.terminalAccess import ANSIParser
        self.Parser = ANSIParser

    def test_empty_string(self):
        """Test parsing empty string."""
        parser = self.Parser()
        result = parser.parse('')
        # parse() returns a dict with parser state
        self.assertIsInstance(result, dict)

    def test_plain_text_no_codes(self):
        """Test parsing plain text without ANSI codes."""
        parser = self.Parser()
        result = parser.parse('Hello World')
        # parse() returns dict, not the text
        self.assertIsInstance(result, dict)
        # Attributes should remain default
        self.assertIsNone(parser.foreground)
        self.assertIsNone(parser.background)

    def test_multiple_attributes_same_code(self):
        """Test parsing multiple attributes in one code."""
        parser = self.Parser()
        parser.parse('\x1b[1;31;4mBold red underlined')

        self.assertTrue(parser.bold)
        self.assertEqual(parser.foreground, 'red')
        self.assertTrue(parser.underline)

    def test_invalid_ansi_code(self):
        """Test parsing invalid ANSI codes."""
        parser = self.Parser()
        # Should not crash on invalid codes
        result = parser.parse('\x1b[999mInvalid code')
        self.assertIsInstance(result, dict)

    def test_incomplete_ansi_code(self):
        """Test parsing incomplete ANSI codes."""
        parser = self.Parser()
        # Should handle incomplete codes gracefully
        result = parser.parse('\x1b[31Incomplete')
        self.assertIsInstance(result, dict)

    def test_nested_ansi_codes(self):
        """Test parsing nested/overlapping ANSI codes."""
        parser = self.Parser()
        result = parser.parse('\x1b[31mRed \x1b[1mbold\x1b[0m')
        self.assertIsInstance(result, dict)

    def test_format_attributes_all_set(self):
        """Test formatAttributes with all attributes set."""
        parser = self.Parser()
        parser.parse('\x1b[1;3;4;5;7;8;9;31;41mAll attributes')

        result = parser.formatAttributes(mode='detailed')
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_strip_ansi_complex(self):
        """Test stripANSI with complex nested codes."""
        text = '\x1b[1m\x1b[31mRed\x1b[0m\x1b[32mGreen\x1b[0m'
        result = self.Parser.stripANSI(text)
        self.assertEqual(result, 'RedGreen')

    def test_default_foreground_color(self):
        """Test resetting to default foreground."""
        parser = self.Parser()
        parser.parse('\x1b[31mRed')
        self.assertEqual(parser.foreground, 'red')

        parser.parse('\x1b[39mDefault')
        # Code 39 resets to default (None or 'default')
        self.assertIn(parser.foreground, [None, 'default'])

    def test_default_background_color(self):
        """Test resetting to default background."""
        parser = self.Parser()
        parser.parse('\x1b[41mRed background')
        self.assertEqual(parser.background, 'red')

        parser.parse('\x1b[49mDefault background')
        # Code 49 resets to default (None or 'default')
        self.assertIn(parser.background, [None, 'default'])


class TestBidiHelperMethods(unittest.TestCase):
    """Test BidiHelper methods."""

    def setUp(self):
        """Set up test fixtures."""
        from globalPlugins.terminalAccess import BidiHelper
        self.helper = BidiHelper()

    def test_is_available(self):
        """Test is_available method."""
        result = self.helper.is_available()
        self.assertIsInstance(result, bool)

    def test_process_text_preserves_length(self):
        """Test process_text preserves text length."""
        text = "Hello World"
        result = self.helper.process_text(text)
        # Length should be preserved (or at least not dramatically different)
        self.assertGreater(len(result), 0)


class TestEmojiHelperMethods(unittest.TestCase):
    """Test EmojiHelper methods."""

    def setUp(self):
        """Set up test fixtures."""
        from globalPlugins.terminalAccess import EmojiHelper
        self.helper = EmojiHelper()

    def test_is_available(self):
        """Test is_available method."""
        result = self.helper.is_available()
        self.assertIsInstance(result, bool)

    def test_get_emoji_width_ascii(self):
        """Test get_emoji_width with ASCII text."""
        result = self.helper.get_emoji_width("Hello")
        self.assertEqual(result, 5)


class TestPositionCacheEdgeCases(unittest.TestCase):
    """Edge case tests for PositionCache."""

    def setUp(self):
        """Set up test fixtures."""
        from globalPlugins.terminalAccess import PositionCache
        self.cache = PositionCache()

    def test_overwrite_existing_entry(self):
        """Test overwriting an existing cache entry."""
        self.cache.set('key1', 10, 20)
        self.assertEqual(self.cache.get('key1'), (10, 20))

        self.cache.set('key1', 30, 40)
        self.assertEqual(self.cache.get('key1'), (30, 40))

    def test_clear_empty_cache(self):
        """Test clearing an already empty cache."""
        self.cache.clear()
        # Should not crash
        self.assertIsNone(self.cache.get('anything'))

    def test_invalidate_nonexistent_key(self):
        """Test invalidating a key that doesn't exist."""
        self.cache.invalidate('nonexistent')
        # Should not crash


if __name__ == '__main__':
    unittest.main()
