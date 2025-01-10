import tkinter as tk
from tkinter import simpledialog

def open_metadata_form(video_path, save_callback):
    """Open a dialog to input metadata for the selected video."""
    metadata_window = tk.Toplevel()  # Create a new window for metadata input
    metadata_window.title("Add Metadata")
    
    # Video path label
    video_path_label = tk.Label(metadata_window, text=f"Video Path: {video_path}")
    video_path_label.pack(pady=10)
    
    # Add metadata fields here (e.g., title, description, etc.)
    title_label = tk.Label(metadata_window, text="Title:")
    title_label.pack(pady=5)
    title_entry = tk.Entry(metadata_window)
    title_entry.pack(pady=5)

    artist_label = tk.Label(metadata_window, text="Artist:")
    artist_label.pack(pady=5)
    artist_entry = tk.Entry(metadata_window)
    artist_entry.pack(pady=5)

    category_label = tk.Label(metadata_window, text="Category:")
    category_label.pack(pady=5)
    category_entry = tk.Entry(metadata_window)
    category_entry.pack(pady=5)

    chord_label = tk.Label(metadata_window, text="Chord:")
    chord_label.pack(pady=5)
    chord_entry = tk.Entry(metadata_window)
    chord_entry.pack(pady=5)

    # Button to save metadata
    save_button = tk.Button(
        metadata_window, 
        text="Save", 
        command=lambda: save_metadata(
            title_entry.get(), artist_entry.get(), 
            category_entry.get(), chord_entry.get(), save_callback
        )
    )
    save_button.pack(pady=10)

    metadata_window.mainloop()

def save_metadata(title, artist, category, chord, save_callback):
    """Save the metadata and pass it to the callback."""
    metadata = {
        "title": title,
        "artist": artist,
        "category": category,
        "chord": chord,
    }
    # Call the provided callback function to save the metadata
    save_callback(metadata)
    print(f"Metadata saved: {metadata}")
