import unittest
from unittest.mock import patch, MagicMock
from modules.folder_upload import VideoUploader
from modules.video_display import display_videos
from modules.category_filter import filter_videos_by_category

class TestModules(unittest.TestCase):
    @patch("modules.folder_upload.os.path")
    def test_folder_upload(self, mock_path):
        mock_path.exists.return_value = True
        mock_uploader = VideoUploader(None, MagicMock())
        self.assertTrue(mock_uploader)

    @patch("modules.video_display.tk.Frame")
    @patch("modules.video_display.Database")
    def test_display_videos(self, mock_db, mock_frame):
        mock_db.get_all_videos.return_value = []
        display_videos(mock_frame, mock_db, "All")
        mock_db.get_all_videos.assert_called_once()

    def test_filter_videos_by_category(self):
        videos = [
            {"name": "Video 1", "category": "Music"},
            {"name": "Video 2", "category": "Studies"},
        ]
        filtered = filter_videos_by_category(videos, "Music")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["name"], "Video 1")

if __name__ == "__main__":
    unittest.main()
