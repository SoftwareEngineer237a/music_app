import os
from PIL import Image, ImageTk
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
from database.database import Database, Video
import ffmpeg
from modules.video_player import get_installed_media_players, open_video_with_player
from modules.metadata_input import open_metadata_form
from modules.category_filter import filter_videos_by_category  # Import the filter function

# Directory where the videos are stored
VIDEO_FOLDER = 'path_to_uploaded_folder'  # Make sure this path is correct

def generate_thumbnail(video_path, thumbnail_path):
    """Generate a thumbnail for the video."""
    print(f"Generating thumbnail for: {video_path}")  # Debug
    try:
        # Check if the file exists
        if not os.path.exists(video_path):
            print(f"Video file not found at: {video_path}")
            return None
        
        if not os.path.exists(os.path.dirname(thumbnail_path)):
            os.makedirs(os.path.dirname(thumbnail_path))
        
        # Using ffmpeg to generate the thumbnail at the 1-second mark
        (
            ffmpeg
            .input(video_path, ss=1)  # Capture at 1-second mark
            .output(thumbnail_path, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        print(f"Thumbnail saved at: {thumbnail_path}")  # Debug
        return thumbnail_path
    except Exception as e:
        print(f"Error generating thumbnail: {e}")  # Debug
        return None

def on_video_click(video_path):
    """Prompt the user to either add metadata or play the video."""
    # Ask the user if they want to add metadata or play the video
    user_choice = messagebox.askquestion("Choose Action", "Do you want to add metadata or play the video?", icon="question")

    if user_choice == "yes":
        # If they choose "Yes", allow them to add metadata
        open_metadata_form(video_path)  # Open the metadata form
    else:
        # If they choose "No", prompt them to select a media player
        open_media_player_selection(video_path)

def open_media_player_selection(video_path):
    """Open a window for the user to select a media player."""
    media_players = get_installed_media_players()

    if media_players:
        # Create a new window to select a media player
        media_player_window = tk.Toplevel()
        media_player_window.title("Select Media Player")

        # Create a label for the window
        label = tk.Label(media_player_window, text="Select a media player to play the video:")
        label.pack(padx=20, pady=10)

        # Create a listbox to display media players
        player_listbox = tk.Listbox(media_player_window, height=6)
        for player in media_players:
            player_listbox.insert(tk.END, player)
        player_listbox.pack(padx=20, pady=10)

        # Function to handle the media player selection
        def on_player_select():
            selected_player = player_listbox.get(tk.ACTIVE)
            if selected_player:
                open_video_with_player(video_path, selected_player)
                media_player_window.destroy()
            else:
                messagebox.showerror("No Selection", "Please select a media player.")

        # Add a "Play" button to confirm the selection
        play_button = tk.Button(media_player_window, text="Play", command=on_player_select)
        play_button.pack(pady=10)

        # Add a "Cancel" button to close the window
        cancel_button = tk.Button(media_player_window, text="Cancel", command=media_player_window.destroy)
        cancel_button.pack(pady=5)

        media_player_window.mainloop()
    else:
        messagebox.showerror("No Media Players Found", "No installed media players were found.")

def fetch_videos_from_folder():
    """Fetch all videos from the uploaded folder."""
    videos = []
    for root, dirs, files in os.walk(VIDEO_FOLDER):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_path = os.path.join(root, file)
                # If the video doesn't already exist in the database, add it
                video = Video(file_name=video_path)
                videos.append(video)
    return videos

def display_videos(video_frame, db, selected_category="All"):
    """Retrieve and display videos in the dashboard with optional category filter."""
    # Clear existing widgets
    for widget in video_frame.winfo_children():
        widget.destroy()

    # Fetch videos from the database
    videos = fetch_videos_from_folder()

    # Apply category filter
    videos = filter_videos_by_category(videos, selected_category)

    if not videos:
        placeholder_label = ctk.CTkLabel(video_frame, text="No videos to display.", anchor="center")
        placeholder_label.pack(fill=tk.BOTH, expand=True)
        return

    print(f"Displaying {len(videos)} videos.")  # Debug: Print the number of videos

    row, col = 0, 0
    for video in videos:
        print(f"Processing video: {video}")  # Debug: Print each video object

        video_path = video.file_name  # Use the `file_name` attribute
        video_name = os.path.basename(video_path)

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
                thumbnail_label = ctk.CTkLabel(video_card, image=img, text="")  # Display thumbnail
                thumbnail_label.image = img  # Prevent garbage collection
                thumbnail_label.pack()

                # Video name
                video_label = ctk.CTkLabel(video_card, text=video.name or video_name, anchor="center")
                video_label.pack()

                # Add a click event to ask the user to either add metadata or play the video
                video_card.bind("<Button-1>", lambda event, video_path=video_path: on_video_click(video_path))

            else:
                print(f"Thumbnail not found for video: {video_path}")  # Debug
        except Exception as e:
            print(f"Error displaying video: {e}")  # Debug

        col += 1
        if col > 3:  # Limit to 4 columns per row
            col = 0
            row += 1
