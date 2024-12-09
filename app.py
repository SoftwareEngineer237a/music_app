import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class VideoTutorialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Tutorial App")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        # Main Frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title Label
        self.title_label = ttk.Label(self.main_frame, text="Video Tutorial App", font=("Helvetica", 24), background="#f0f0f0")
        self.title_label.pack(pady=20)

        # Folder Selection Section
        self.folder_button = ttk.Button(self.main_frame, text="Upload Video Folder", command=self.upload_folder)
        self.folder_button.pack(pady=10)

        self.selected_folder_label = ttk.Label(self.main_frame, text="No folder selected", font=("Helvetica", 12), background="#f0f0f0")
        self.selected_folder_label.pack(pady=10)

        # Video List Section
        self.video_list_label = ttk.Label(self.main_frame, text="Videos Found:", font=("Helvetica", 14), background="#f0f0f0")
        self.video_list_label.pack(pady=10)

        self.video_listbox = tk.Listbox(self.main_frame, width=50, height=10)
        self.video_listbox.pack(pady=10)

        self.add_metadata_button = ttk.Button(self.main_frame, text="Add Metadata", command=self.add_metadata)
        self.add_metadata_button.pack(pady=10)

        # Footer
        self.footer_label = ttk.Label(self.main_frame, text="© 2024 Video Tutorial App", font=("Helvetica", 10), background="#f0f0f0")
        self.footer_label.pack(side=tk.BOTTOM, pady=10)

        # Store video metadata
        self.video_metadata = {}

    def upload_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.selected_folder_label.config(text=f"Selected Folder: {folder_path}")
            self.populate_video_list(folder_path)
        else:
            messagebox.showinfo("Info", "No folder selected.")

    def populate_video_list(self, folder_path):
        # Clear the current list
        self.video_listbox.delete(0, tk.END)

        # Supported video file extensions
        video_extensions = ('.mp4', '.mkv', '.avi', '.mov', '.wmv')

        # Scan the folder for video files
        for filename in os.listdir(folder_path):
            if filename.endswith(video_extensions):
                self.video_listbox.insert(tk.END, filename)

    def add_metadata(self):
        selected_video = self.video_listbox.curselection()
        if not selected_video:
            messagebox.showinfo("Info", "Please select a video from the list.")
            return

        video_name = self.video_listbox.get(selected_video)
        
        # Create a new window for metadata input
        metadata_window = tk.Toplevel(self.root)
        metadata_window.title("Enter Video Metadata")
        metadata_window.geometry("300x400")

        ttk.Label(metadata_window, text="Enter Metadata for: " + video_name).pack(pady=10)

        # Inputs for metadata
        self.name_entry = ttk.Entry(metadata_window, width=30)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Video Name")

        self.artist_entry = ttk.Entry(metadata_window, width=30)
        self.artist_entry.pack(pady=5)
        self.artist_entry.insert(0, "Artist")

        self.title_entry = ttk.Entry(metadata_window, width=30)
        self.title_entry.pack(pady=5)
        self.title_entry.insert(0, "Title")

        self.category_entry = ttk.Entry(metadata_window, width=30)
        self.category_entry.pack(pady=5)
        self.category_entry.insert(0, "Category")

        self.chord_entry = ttk.Entry(metadata_window, width=30)
        self.chord_entry.pack(pady=5)
        self.chord_entry.insert(0, "Chord")

        save_button = ttk.Button(metadata_window, text="Save Metadata", command=lambda: self.save_metadata(video_name))
        save_button.pack(pady=10)

    def save_metadata(self, video_name):
        # Save the metadata entered by the user
        metadata = {
            'name': self.name_entry.get(),
            'artist': self.artist_entry.get(),
            'title': self.title_entry.get(),
            'category': self.category_entry.get(),
            'chord': self.chord_entry.get()
        }

        # Store the metadata in the dictionary
        self.video_metadata[video_name] = metadata
        messagebox.showinfo("Success", "Metadata saved successfully!")
        print(self.video_metadata)  # For debugging; can be removed later

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoTutorialApp(root)
    root.mainloop()