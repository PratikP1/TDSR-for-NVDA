"""
Tests for terminal window recognition bug fix.

Tests that isTerminalApp properly handles edge cases where obj.appModule.appName
doesn't exist or raises AttributeError.
"""
import unittest
from unittest.mock import Mock, MagicMock, PropertyMock, patch


class TestTerminalRecognitionFix(unittest.TestCase):
	"""Test terminal recognition with various edge cases."""

	def setUp(self):
		"""Set up test fixtures."""
		from globalPlugins.terminalAccess import GlobalPlugin
		with patch('gui.settingsDialogs.NVDASettingsDialog'):
			self.plugin = GlobalPlugin()

	def test_isterminalapp_with_none_obj(self):
		"""Test isTerminalApp with None object."""
		with patch('api.getForegroundObject', return_value=None):
			result = self.plugin.isTerminalApp(None)
			self.assertFalse(result)

	def test_isterminalapp_with_none_appmodule(self):
		"""Test isTerminalApp with None appModule."""
		mock_obj = Mock()
		mock_obj.appModule = None
		result = self.plugin.isTerminalApp(mock_obj)
		self.assertFalse(result)

	def test_isterminalapp_with_missing_appname(self):
		"""Test isTerminalApp when appModule has no appName attribute."""
		mock_obj = Mock()
		mock_obj.appModule = Mock(spec=[])  # Empty spec means no attributes
		result = self.plugin.isTerminalApp(mock_obj)
		self.assertFalse(result)

	def test_isterminalapp_with_appname_raising_attributeerror(self):
		"""Test isTerminalApp when accessing appName raises AttributeError."""
		mock_obj = Mock()
		mock_obj.appModule = Mock()
		# Make appName raise AttributeError when accessed
		type(mock_obj.appModule).appName = PropertyMock(side_effect=AttributeError("No appName"))
		result = self.plugin.isTerminalApp(mock_obj)
		self.assertFalse(result)

	def test_isterminalapp_with_appname_raising_typeerror(self):
		"""Test isTerminalApp when accessing appName raises TypeError."""
		mock_obj = Mock()
		mock_obj.appModule = Mock()
		# Make appName raise TypeError when accessed
		type(mock_obj.appModule).appName = PropertyMock(side_effect=TypeError("Type error"))
		result = self.plugin.isTerminalApp(mock_obj)
		self.assertFalse(result)

	def test_isterminalapp_with_valid_windowsterminal(self):
		"""Test isTerminalApp with valid Windows Terminal."""
		mock_obj = Mock()
		mock_obj.appModule = Mock()
		mock_obj.appModule.appName = "WindowsTerminal"
		result = self.plugin.isTerminalApp(mock_obj)
		self.assertTrue(result)

	def test_isterminalapp_with_valid_cmd(self):
		"""Test isTerminalApp with valid cmd.exe."""
		mock_obj = Mock()
		mock_obj.appModule = Mock()
		mock_obj.appModule.appName = "cmd"
		result = self.plugin.isTerminalApp(mock_obj)
		self.assertTrue(result)

	def test_isterminalapp_with_valid_powershell(self):
		"""Test isTerminalApp with valid PowerShell."""
		mock_obj = Mock()
		mock_obj.appModule = Mock()
		mock_obj.appModule.appName = "powershell"
		result = self.plugin.isTerminalApp(mock_obj)
		self.assertTrue(result)

	def test_isterminalapp_with_non_terminal_app(self):
		"""Test isTerminalApp with non-terminal application."""
		mock_obj = Mock()
		mock_obj.appModule = Mock()
		mock_obj.appModule.appName = "notepad"
		result = self.plugin.isTerminalApp(mock_obj)
		self.assertFalse(result)

	def test_isterminalapp_case_insensitive(self):
		"""Test isTerminalApp is case insensitive."""
		mock_obj = Mock()
		mock_obj.appModule = Mock()
		# Test with uppercase
		mock_obj.appModule.appName = "CMD"
		result = self.plugin.isTerminalApp(mock_obj)
		self.assertTrue(result)

		# Test with mixed case
		mock_obj.appModule.appName = "PowerShell"
		result = self.plugin.isTerminalApp(mock_obj)
		self.assertTrue(result)

	def test_event_gainfocus_with_missing_appname(self):
		"""Test event_gainFocus handles missing appName gracefully."""
		mock_obj = Mock()
		mock_obj.appModule = Mock(spec=[])  # No appName attribute
		mock_nextHandler = Mock()

		# Patch isTerminalApp to return True to test the appName access
		with patch.object(self.plugin, 'isTerminalApp', return_value=True):
			# This should not raise an exception
			self.plugin.event_gainFocus(mock_obj, mock_nextHandler)
			# Verify nextHandler was called
			mock_nextHandler.assert_called_once()

	def test_event_gainfocus_with_appname_raising_error(self):
		"""Test event_gainFocus handles appName AttributeError gracefully."""
		mock_obj = Mock()
		mock_obj.appModule = Mock()
		type(mock_obj.appModule).appName = PropertyMock(side_effect=AttributeError("No appName"))
		mock_nextHandler = Mock()

		# Patch isTerminalApp to return True to test the appName access
		with patch.object(self.plugin, 'isTerminalApp', return_value=True):
			# This should not raise an exception
			self.plugin.event_gainFocus(mock_obj, mock_nextHandler)
			# Verify nextHandler was called
			mock_nextHandler.assert_called_once()


if __name__ == '__main__':
	unittest.main()
