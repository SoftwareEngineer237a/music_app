import os
from PIL import Image, ImageTk
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from database.database import Database
from modules.video_player import play_video  # Assuming there's a play_video function in video_player.py

def generate_thumbnail(video_path, thumbnail_path):
    """Generate a thumbnail for the video."""
    print(f"Generating thumbnail for: {video_path}")  # Debug
    try:
        if not os.path.exists(os.path.dirname(thumbnail_path)):
            os.makedirs(os.path.dirname(thumbnail_path))
        # Logic for generating thumbnails (you can use ffmpeg or another method)
        thumbnail_path = video_path.replace(".mp4", "_thumbnail.jpg")  # Example
        # Use ffmpeg or PIL to generate the thumbnail
        return thumbnail_path
    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        return None

def display_videos(video_frame, db: Database):
    """Fetch and display videos in the dashboard."""
    for widget in video_frame.winfo_children():
        widget.destroy()  # Clear existing widgets

    videos = db.fetch_videos()
    print(f"Displaying {len(videos)} videos.")  # Debug

    if not videos:
        placeholder_label = ctk.CTkLabel(video_frame, text="No videos to display.", anchor="center")
        placeholder_label.pack(fill=tk.BOTH, expand=True)
        return

    row, col = 0, 0
    for video in videos:
        print(f"Processing video: {video}")  # Debug
        video_path = video[1]  # Assuming file_path is the second column
        video_name = os.path.basename(video_path)  # Use base name for thumbnail

        # Generate or locate the thumbnail
        thumbnail_path = f"temp_thumbnails/{video_name}.jpg"
        if not os.path.exists(thumbnail_path):
            thumbnail_path = generate_thumbnail(video_path, thumbnail_path)

        # Load thumbnail and display
        try:
            if thumbnail_path and os.path.exists(thumbnail_path):
                img = Image.open(thumbnail_path)
                img = img.resize((200, 150), Image.ANTIALIAS)  # Resize for consistency
                img = ImageTk.PhotoImage(img)

                # Create a frame for each video
                video_card = ctk.CTkFrame(video_frame, width=220, height=200)
                video_card.grid(row=row, column=col, padx=10, pady=10)

                # Thumbnail image
                thumbnail_label = ctk.CTkLabel(video_card, image=img, text="")
                thumbnail_label.image = img  # Prevent garbage collection
                thumbnail_label.pack()

                # Video name
                video_label = ctk.CTkLabel(video_card, text=video_name, anchor="center")
                video_label.pack()
            else:
                print(f"Thumbnail not found for video: {video_path}")  # Debug
        except Exception as e:
            print(f"Error displaying video: {e}")  # Debug

        col += 1
        if col > 3:  # Limit to 4 columns
            col = 0
            row += 1
