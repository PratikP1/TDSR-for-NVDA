"""
Tests for the Enter-key blank-announcement suppression in _announceStandardCursor.

After the user presses Enter (carriage return), the caret moves to a new empty
line before the terminal has rendered output.  _announceStandardCursor must
suppress the "Blank" announcement for a short window (~300 ms) to avoid
disrupting the user with a premature blank speech message.

Navigation scripts (script_moveTo*) are NOT affected by this suppression.
"""

import time
import unittest
from unittest.mock import MagicMock, patch


class TestEnterBlankSuppression(unittest.TestCase):
	"""Tests for the Enter-key blank-announcement suppression."""

	# ------------------------------------------------------------------
	# Helpers
	# ------------------------------------------------------------------

	def _make_plugin_with_cursor(self, char_at_caret, caret_offset=100):
		"""
		Build a GlobalPlugin instance whose _announceStandardCursor will
		report *char_at_caret* for the character under the caret.

		Returns (plugin, mock_obj) so tests can call
		plugin._announceStandardCursor(mock_obj) directly.
		"""
		from globalPlugins.terminalAccess import GlobalPlugin

		plugin = GlobalPlugin()

		# Provide a mock terminal object whose makeTextInfo returns a
		# TextInfo-like object.
		mock_info = MagicMock()
		mock_info.bookmark.startOffset = caret_offset
		# Ensure cache miss so the code always reads the character.
		plugin._lastLineText = None
		plugin._lastCaretPosition = None  # force position change detection

		# Expand to UNIT_CHARACTER yields the test character.
		def expand_side_effect(unit):
			mock_info.text = char_at_caret

		mock_info.expand.side_effect = expand_side_effect

		# Refreshing the line cache.
		mock_line_info = MagicMock()
		mock_line_info.text = char_at_caret
		mock_line_info.bookmark.startOffset = caret_offset
		mock_line_info.bookmark.endOffset = caret_offset + 1

		def make_text_info(pos):
			info = MagicMock()
			info.bookmark.startOffset = caret_offset
			info.expand.side_effect = expand_side_effect
			info.text = char_at_caret
			return info

		mock_obj = MagicMock()
		mock_obj.makeTextInfo.side_effect = make_text_info

		return plugin, mock_obj

	# ------------------------------------------------------------------
	# _lastEnterTime initialization
	# ------------------------------------------------------------------

	def test_last_enter_time_initialized_to_none(self):
		"""_lastEnterTime must start as None so no suppression happens on boot."""
		from globalPlugins.terminalAccess import GlobalPlugin

		plugin = GlobalPlugin()
		self.assertIsNone(plugin._lastEnterTime)

	# ------------------------------------------------------------------
	# event_typedCharacter tracks Enter presses
	# ------------------------------------------------------------------

	@patch('globalPlugins.terminalAccess.ui')
	@patch('globalPlugins.terminalAccess.config')
	def test_event_typedCharacter_sets_last_enter_time_on_cr(self, mock_config, mock_ui):
		"""Typing \\r (carriage return / Enter) must record _lastEnterTime."""
		from globalPlugins.terminalAccess import GlobalPlugin

		plugin = GlobalPlugin()
		mock_config.conf.__getitem__.return_value.__getitem__.return_value = False

		mock_obj = MagicMock()
		before = time.time()
		with patch.object(plugin, 'isTerminalApp', return_value=True):
			plugin.event_typedCharacter(mock_obj, lambda: None, '\r')
		after = time.time()

		self.assertIsNotNone(plugin._lastEnterTime)
		self.assertGreaterEqual(plugin._lastEnterTime, before)
		self.assertLessEqual(plugin._lastEnterTime, after)

	@patch('globalPlugins.terminalAccess.ui')
	@patch('globalPlugins.terminalAccess.config')
	def test_event_typedCharacter_does_not_set_enter_time_for_other_chars(
		self, mock_config, mock_ui
	):
		"""Typing a normal character must NOT update _lastEnterTime."""
		from globalPlugins.terminalAccess import GlobalPlugin

		plugin = GlobalPlugin()
		mock_config.conf.__getitem__.return_value.__getitem__.return_value = False

		mock_obj = MagicMock()
		with patch.object(plugin, 'isTerminalApp', return_value=True):
			plugin.event_typedCharacter(mock_obj, lambda: None, 'a')

		self.assertIsNone(plugin._lastEnterTime)

	# ------------------------------------------------------------------
	# _announceStandardCursor suppression within window
	# ------------------------------------------------------------------

	@patch('globalPlugins.terminalAccess.ui')
	def test_blank_suppressed_within_300ms_of_enter(self, mock_ui):
		"""Blank must NOT be announced when Enter was pressed <300 ms ago."""
		plugin, mock_obj = self._make_plugin_with_cursor('')

		# Simulate a very recent Enter press.
		plugin._lastEnterTime = time.time()

		plugin._announceStandardCursor(mock_obj)

		mock_ui.message.assert_not_called()

	@patch('globalPlugins.terminalAccess.ui')
	def test_newline_char_suppressed_within_300ms_of_enter(self, mock_ui):
		"""\\n at caret must NOT be announced within 300 ms of Enter."""
		plugin, mock_obj = self._make_plugin_with_cursor('\n')

		plugin._lastEnterTime = time.time()

		plugin._announceStandardCursor(mock_obj)

		mock_ui.message.assert_not_called()

	@patch('globalPlugins.terminalAccess.ui')
	def test_cr_char_suppressed_within_300ms_of_enter(self, mock_ui):
		"""\\r at caret must NOT be announced within 300 ms of Enter."""
		plugin, mock_obj = self._make_plugin_with_cursor('\r')

		plugin._lastEnterTime = time.time()

		plugin._announceStandardCursor(mock_obj)

		mock_ui.message.assert_not_called()

	# ------------------------------------------------------------------
	# _announceStandardCursor announces Blank outside the window
	# ------------------------------------------------------------------

	@patch('globalPlugins.terminalAccess.ui')
	def test_blank_announced_when_enter_not_pressed(self, mock_ui):
		"""Blank must be announced when Enter was never pressed."""
		plugin, mock_obj = self._make_plugin_with_cursor('')

		# _lastEnterTime stays None.
		plugin._announceStandardCursor(mock_obj)

		mock_ui.message.assert_called_once()
		args = mock_ui.message.call_args[0]
		self.assertIn("blank", args[0].lower())

	@patch('globalPlugins.terminalAccess.ui')
	def test_blank_announced_after_suppression_window_expires(self, mock_ui):
		"""Blank must be announced once the 300 ms suppression window has passed."""
		plugin, mock_obj = self._make_plugin_with_cursor('')

		# Simulate an Enter press that happened more than 300 ms ago.
		plugin._lastEnterTime = time.time() - 0.4

		plugin._announceStandardCursor(mock_obj)

		mock_ui.message.assert_called_once()
		args = mock_ui.message.call_args[0]
		self.assertIn("blank", args[0].lower())

	# ------------------------------------------------------------------
	# Normal characters are never suppressed
	# ------------------------------------------------------------------

	@patch('globalPlugins.terminalAccess.ui')
	def test_normal_char_always_announced_even_after_enter(self, mock_ui):
		"""A printable character at the caret must always be announced."""
		plugin, mock_obj = self._make_plugin_with_cursor('a')

		plugin._lastEnterTime = time.time()

		plugin._announceStandardCursor(mock_obj)

		mock_ui.message.assert_called_once()
		self.assertEqual(mock_ui.message.call_args[0][0], 'a')

	@patch('globalPlugins.terminalAccess.ui')
	def test_space_char_always_announced_even_after_enter(self, mock_ui):
		"""Space at the caret must still be announced after Enter."""
		plugin, mock_obj = self._make_plugin_with_cursor(' ')

		plugin._lastEnterTime = time.time()

		plugin._announceStandardCursor(mock_obj)

		mock_ui.message.assert_called_once()


if __name__ == '__main__':
	unittest.main()
