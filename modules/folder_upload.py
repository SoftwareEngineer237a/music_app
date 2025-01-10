# import cv2
# import os
# import customtkinter as ctk
# from tkinter import filedialog
# from PIL import Image, ImageTk

# class VideoUploader:
#     def __init__(self, video_frame, selected_video):
#         self.video_frame = video_frame
#         self.selected_video = selected_video
#         self.video_list = []

#     def upload_folder(self):
#         """Open folder selection dialog and process video files."""
#         folder_path = filedialog.askdirectory(title="Select a Folder")
#         if folder_path:
#             self.video_list = self.scan_folder_for_videos(folder_path)
#             self.update_video_list()
#         else:
#             print("No folder selected.")

#     def scan_folder_for_videos(self, folder_path):
#         """Scan the selected folder for video files."""
#         video_extensions = ('.mp4', '.avi', '.mov', '.mkv')  # Add other formats as needed
#         return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(video_extensions)]

#     def update_video_list(self):
#         """Update the video list display."""
#         for widget in self.video_frame.winfo_children():
#             widget.destroy()  # Clear the video frame

#         if self.video_list:
#             scroll_frame = ctk.CTkScrollableFrame(self.video_frame, width=200)
#             scroll_frame.pack(fill='both', expand=True, padx=5, pady=5)
#             for video in self.video_list:
#                 video_button = ctk.CTkButton(
#                     scroll_frame, text=os.path.basename(video),
#                     command=lambda v=video: self.update_selected_video(v)
#                 )
#                 video_button.pack(pady=2)

#             # Display thumbnail of the first video by default
#             self.display_thumbnail(self.video_list[0])
#         else:
#             placeholder_label = ctk.CTkLabel(self.video_frame, text="No videos found in the selected folder.")
#             placeholder_label.pack(fill='both', expand=True)


#     def update_selected_video(self, listbox):
#         """Update the selected video variable."""
#         selection = listbox.curselection()
#         if selection:
#             self.selected_video.set(self.video_list[selection[0]])

#     def display_thumbnail(self, video_path):
#         """Capture and display a thumbnail from the selected video."""
#         thumbnail = self.capture_thumbnail(video_path)
#         if thumbnail:
#             img = ImageTk.PhotoImage(thumbnail)
#             label = ctk.CTkLabel(self.video_frame, image=img, text="")
#             label.image = img  # Keep a reference!
#             label.pack(pady=10)


#     def capture_thumbnail(self, video_path):
#         """Capture a frame from the specified video file."""
#         cap = cv2.VideoCapture(video_path)
#         cap.set(cv2.CAP_PROP_POS_FRAMES, 100)  # Capture frame at 100th position
#         ret, frame = cap.read()
#         cap.release()
        
#         if ret:
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
#             return Image.fromarray(frame)
        
#         return None

import cv2
import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk

class VideoUploader:
    def __init__(self, video_frame, selected_video):
        self.video_frame = video_frame
        self.selected_video = selected_video
        self.video_list = []

    def upload_folder(self):
        """Open folder selection dialog and process video files."""
        folder_path = filedialog.askdirectory(title="Select a Folder")
        if folder_path:
            self.video_list = self.scan_folder_for_videos(folder_path)
            if self.video_list:
                self.update_video_list()
            else:
                self.display_placeholder("No videos found in the selected folder.")
        else:
            print("No folder selected.")

    def upload_file(self):
        """Open file selection dialog to upload a single video."""
        file_path = filedialog.askopenfilename(
            title="Select a Video File",
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")]
        )
        if file_path:
            self.video_list = [file_path]  # Single file replaces the current list
            self.update_video_list()
        else:
            print("No file selected.")

    def scan_folder_for_videos(self, folder_path):
        """Scan the selected folder for video files."""
        video_extensions = ('.mp4', '.avi', '.mov', '.mkv')  # Add other formats as needed
        return [
            os.path.join(folder_path, f) 
            for f in os.listdir(folder_path) 
            if f.lower().endswith(video_extensions)
        ]

    def update_video_list(self):
        """Update the video list display."""
        for widget in self.video_frame.winfo_children():
            widget.destroy()  # Clear the video frame

        if self.video_list:
            scroll_frame = ctk.CTkScrollableFrame(self.video_frame, width=200)
            scroll_frame.pack(fill='both', expand=True, padx=5, pady=5)
            for video in self.video_list:
                video_button = ctk.CTkButton(
                    scroll_frame, text=os.path.basename(video),
                    command=lambda v=video: self.update_selected_video(v)
                )
                video_button.pack(pady=2)

            # Display thumbnail of the first video by default
            self.display_thumbnail(self.video_list[0])
        else:
            self.display_placeholder("No videos to display.")

    def update_selected_video(self, video):
        """Update the selected video variable."""
        self.selected_video.set(video)
        print(f"Selected video: {video}")

    def display_thumbnail(self, video_path):
        """Capture and display a thumbnail from the selected video."""
        thumbnail = self.capture_thumbnail(video_path)
        if thumbnail:
            img = ImageTk.PhotoImage(thumbnail)
            label = ctk.CTkLabel(self.video_frame, image=img, text="")
            label.image = img  # Keep a reference!
            label.pack(pady=10)
        else:
            self.display_placeholder("Unable to generate thumbnail.")

    def capture_thumbnail(self, video_path):
        """Capture a frame from the specified video file."""
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 100)  # Capture frame at 100th position
        ret, frame = cap.read()
        cap.release()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            return Image.fromarray(frame)

        return None

    def display_placeholder(self, message):
        """Display a placeholder message in the video frame."""
        for widget in self.video_frame.winfo_children():
            widget.destroy()  # Clear the video frame
        placeholder_label = ctk.CTkLabel(self.video_frame, text=message)
        placeholder_label.pack(fill='both', expand=True)
    