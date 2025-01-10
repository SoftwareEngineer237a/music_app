import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from modules.folder_upload import VideoUploader
from database.database import Database
from modules.category_filter import filter_videos_by_category
from modules.video_display import display_videos
from modules.video_player import open_video_with_player
from modules.track_status import VideoStatusUI  # Import VideoStatusUI
from modules.favorites import FavoritesDatabase  # Import FavoritesDatabase class from favorites.py


def setup_database():
    """Initialize the database with schema."""
    db = Database()  # Initialize Database class (using SQLAlchemy)
    db.initialize_database()  # Ensure the schema is created
    return db


def open_metadata_form(selected_video, db):
    """Open a form to input metadata for the selected video."""
    if not selected_video:
        messagebox.showerror("Error", "No video selected.")
        return

    metadata_window = tk.Toplevel()
    metadata_window.title("Add Metadata")
    metadata_window.geometry("400x300")

    tk.Label(metadata_window, text=f"File: {selected_video}").pack(pady=5)

    fields = {
        "Name": tk.Entry(metadata_window),
        "Artist": tk.Entry(metadata_window),
        "Title": tk.Entry(metadata_window),
        "Category": tk.Entry(metadata_window),
        "Chord": tk.Entry(metadata_window),
    }

    for label, entry in fields.items():
        tk.Label(metadata_window, text=f"{label}:").pack()
        entry.pack()

    def submit_metadata():
        metadata = {
            "filename": selected_video,
            **{key.lower(): entry.get().strip() for key, entry in fields.items()},
        }
        if any(value == "" for value in metadata.values()):
            messagebox.showerror("Error", "All fields must be filled.")
            return

        db.add_video(selected_video, metadata)
        messagebox.showinfo("Success", "Metadata added successfully!")
        metadata_window.destroy()

    tk.Button(metadata_window, text="Submit", command=submit_metadata).pack(pady=10)


def open_media_player_selection(video_path):
    """Open a window for the user to select a media player."""
    media_players = ["VLC Media Player", "Windows Media Player", "Movies & TV"]  # Simplified for this example

    if not media_players:
        messagebox.showerror("Error", "No media players found.")
        return

    media_player_window = tk.Toplevel()
    media_player_window.title("Select Media Player")
    tk.Label(media_player_window, text="Select a media player to play the video:").pack(pady=10)

    listbox = tk.Listbox(media_player_window)
    for player in media_players:
        listbox.insert(tk.END, player)
    listbox.pack(pady=10)

    def play_video():
        selected_player = listbox.get(tk.ACTIVE)
        if selected_player:
            open_video_with_player(video_path, selected_player)
            media_player_window.destroy()
        else:
            messagebox.showerror("Error", "Please select a media player.")

    tk.Button(media_player_window, text="Play", command=play_video).pack(pady=5)
    tk.Button(media_player_window, text="Cancel", command=media_player_window.destroy).pack(pady=5)


def create_main_window():
    """Main application window."""
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Music Tracker")
    root.geometry("900x600")

    db = setup_database()
    favorites_db = FavoritesDatabase()  # Initialize FavoritesDatabase

    selected_video = tk.StringVar()  # Variable to hold the selected video path

    # Navigation bar
    nav_frame = ctk.CTkFrame(root, height=50)
    nav_frame.pack(fill=tk.X)

    video_frame = ctk.CTkFrame(root)
    video_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    uploader = VideoUploader(video_frame, selected_video)

    # Category dropdown
    category_options = ["All", "Music", "Studies", "Football"]
    category_dropdown = ctk.CTkOptionMenu(
        nav_frame, values=category_options,
        command=lambda category: display_videos(video_frame, db, category)
    )
    category_dropdown.pack(side=tk.LEFT, padx=10, pady=10)

    # Buttons
    ctk.CTkButton(nav_frame, text="Dashboard",
                  command=lambda: display_videos(video_frame, db, "All")).pack(side=tk.LEFT, padx=10, pady=10)

    ctk.CTkButton(nav_frame, text="Upload Folder", command=uploader.upload_folder).pack(side=tk.LEFT, padx=10, pady=10)
    ctk.CTkButton(nav_frame, text="Upload File", command=uploader.upload_file).pack(side=tk.LEFT, padx=10, pady=10)

    ctk.CTkButton(nav_frame, text="Add Metadata",
                  command=lambda: open_metadata_form(selected_video.get(), db)).pack(side=tk.LEFT, padx=10, pady=10)

    ctk.CTkButton(nav_frame, text="Play",
                  command=lambda: open_media_player_selection(selected_video.get())).pack(side=tk.LEFT, padx=10, pady=10)

    # Add Favorites Buttons
    ctk.CTkButton(nav_frame, text="Add to Favorites",
                  command=lambda: favorites_db.add_to_favorites(1)).pack(side=tk.LEFT, padx=10, pady=10)  # Example: Replace 1 with the selected video ID

    ctk.CTkButton(nav_frame, text="View Favorites",
                  command=lambda: view_favorites(favorites_db)).pack(side=tk.LEFT, padx=10, pady=10)

    # Initialize the video status management UI
    video_list = ["video1.mp4", "video2.mp4", "video3.mkv"]  # Replace this with the actual video list
    VideoStatusUI(root, db, video_list)  # Add the status management UI here

    display_videos(video_frame, db, "All")  # Initial display of videos
    root.mainloop()


def view_favorites(favorites_db):
    """Display the list of favorite videos."""
    favorite_videos = favorites_db.get_favorite_videos()
    if favorite_videos:
        favorite_video_names = [video.name for video in favorite_videos]
        messagebox.showinfo("Favorite Videos", "\n".join(favorite_video_names))
    else:
        messagebox.showinfo("Favorite Videos", "No favorite videos found.")


if __name__ == "__main__":
    create_main_window()
