import tkinter as tk
from tkinter import messagebox
from database.database import Database

class VideoStatus:
    def __init__(self, db: Database):
        self.db = db

    def mark_as_read(self, video_path):
        """Mark a video as read and update the database."""
        try:
            # Update the video's status in the database
            video = self.db.get_video_by_filename(video_path)
            if video:
                video.status = "read"  # Update status to "read"
                self.db.commit()
                messagebox.showinfo("Success", f"The video '{video_path}' has been marked as read.")
            else:
                messagebox.showerror("Error", f"Video '{video_path}' not found in the database.")
        except Exception as e:
            messagebox.showerror("Error", f"Error marking video as read: {str(e)}")

    def mark_as_unread(self, video_path):
        """Mark a video as unread and update the database."""
        try:
            # Update the video's status in the database
            video = self.db.get_video_by_filename(video_path)
            if video:
                video.status = "unread"  # Update status to "unread"
                self.db.commit()
                messagebox.showinfo("Success", f"The video '{video_path}' has been marked as unread.")
            else:
                messagebox.showerror("Error", f"Video '{video_path}' not found in the database.")
        except Exception as e:
            messagebox.showerror("Error", f"Error marking video as unread: {str(e)}")

    def get_video_status(self, video_path):
        """Get the status of a video."""
        video = self.db.get_video_by_filename(video_path)
        return video.status if video else None


class VideoStatusUI:
    def __init__(self, root, db: Database, video_list):
        self.db = db
        self.video_status = VideoStatus(db)
        self.video_list = video_list
        self.root = root
        self._create_video_status_ui()

    def _create_video_status_ui(self):
        """Create the UI to display and update the video read/unread status."""
        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=10)

        tk.Label(status_frame, text="Mark Videos as Read/Unread").pack(pady=5)

        self.status_buttons = {}

        for video in self.video_list:
            video_status = self.video_status.get_video_status(video)
            status_btn_text = f"{video} - {video_status}" if video_status else f"{video} - Unread"
            status_button = tk.Button(status_frame, text=status_btn_text, 
                                      command=lambda video=video: self.toggle_video_status(video))
            status_button.pack(pady=5)
            self.status_buttons[video] = status_button

    def toggle_video_status(self, video_path):
        """Toggle the status of the selected video between 'read' and 'unread'."""
        current_status = self.video_status.get_video_status(video_path)
        if current_status == "read":
            self.video_status.mark_as_unread(video_path)
        else:
            self.video_status.mark_as_read(video_path)

        # Update the UI button text after the status change
        new_status = self.video_status.get_video_status(video_path)
        self.status_buttons[video_path].config(text=f"{video_path} - {new_status}")
