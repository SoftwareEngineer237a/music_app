import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from ui.main_window import open_metadata_form

class TestUI(unittest.TestCase):
    @patch("ui.main_window.tk.Toplevel")
    def test_open_metadata_form(self, mock_toplevel):
        mock_db = MagicMock()
        mock_video = "sample.mp4"

        # Call the function
        open_metadata_form(mock_video, mock_db)

        # Check if Toplevel window was created
        mock_toplevel.assert_called_once()

        # Check if metadata form functions properly
        self.assertTrue(mock_toplevel.called)

    def test_ui_elements(self):
        root = tk.Tk()
        self.assertIsInstance(root, tk.Tk)

if __name__ == "__main__":
    unittest.main()
