import unittest
from unittest.mock import patch, MagicMock
from database.database import Database, Video

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database(':memory:')  # Use an in-memory SQLite database for testing

    def tearDown(self):
        self.db.close()

    def test_add_video(self):
        metadata = {
            "name": "Sample Video",
            "artist": "Sample Artist",
            "title": "Sample Title",
            "category": "Music",
            "chord": "C",
        }
        self.db.add_video("sample.mp4", metadata)
        video = self.db.get_video_by_filename("sample.mp4")
        self.assertIsNotNone(video)
        self.assertEqual(video.name, "Sample Video")

    def test_fetch_all_videos(self):
        self.db.add_video("video1.mp4", {"name": "Video 1", "artist": "Artist", "title": "Title", "category": "Music", "chord": "C"})
        self.db.add_video("video2.mp4", {"name": "Video 2", "artist": "Artist", "title": "Title", "category": "Studies", "chord": "D"})
        videos = self.db.get_all_videos()
        self.assertEqual(len(videos), 2)

    def test_fetch_videos_by_category(self):
        self.db.add_video("video1.mp4", {"name": "Video 1", "artist": "Artist", "title": "Title", "category": "Music", "chord": "C"})
        self.db.add_video("video2.mp4", {"name": "Video 2", "artist": "Artist", "title": "Title", "category": "Studies", "chord": "D"})
        music_videos = self.db.fetch_videos_by_category("Music")
        self.assertEqual(len(music_videos), 1)

    def test_delete_video(self):
        self.db.add_video("video1.mp4", {"name": "Video 1", "artist": "Artist", "title": "Title", "category": "Music", "chord": "C"})
        video = self.db.get_video_by_filename("video1.mp4")
        self.assertIsNotNone(video)
        self.db.delete_video(video.id)
        video = self.db.get_video_by_filename("video1.mp4")
        self.assertIsNone(video)

if __name__ == "__main__":
    unittest.main()
