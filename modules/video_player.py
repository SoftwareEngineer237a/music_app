# import psutil
# import subprocess
# import tkinter as tk
# from tkinter import simpledialog, messagebox

# def get_installed_media_players():
#     """List common installed media players on the system."""
#     players = []

#     # Check for common media player executables in system PATH
#     media_players = [
#         "vlc", "mplayer", "mpv", "windowsmedia", "quicktime", "potplayer", "gplayer", "realplayer"
#     ]

#     for player in media_players:
#         try:
#             # Try to get the media player's executable path
#             process = psutil.process_iter(attrs=['name'])
#             for proc in process:
#                 if player.lower() in proc.info['name'].lower():
#                     players.append(player)
#                     break
#         except (psutil.NoSuchProcess, psutil.AccessDenied):
#             continue

#     # If no players are found, check system PATH for executable presence
#     for player in media_players:
#         if player.lower() not in [p.lower() for p in players]:
#             try:
#                 subprocess.run([player, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#                 players.append(player)  # If subprocess runs successfully, add to list
#             except Exception as e:
#                 continue

#     return players

# def open_video_with_player(video_path, player_name):
#     """Open the video using the selected media player."""
#     try:
#         # If media player is available in PATH, execute it with the video file
#         process = subprocess.run([player_name, video_path], check=True)
#         if process.returncode == 0:
#             print(f"Successfully opened {video_path} with {player_name}.")
#         else:
#             print(f"Error: {player_name} failed to open the video.")
#     except FileNotFoundError:
#         messagebox.showerror("Error", f"The media player {player_name} could not be found.")
#     except Exception as e:
#         messagebox.showerror("Error", f"Error opening video with {player_name}: {e}")
import os
import psutil
import subprocess
from tkinter import messagebox
import tkinter as tk


def get_installed_media_players():
    """Dynamically detect installed media players on the system."""
    players = []

    # Common media players we want to check for
    potential_players = [
        "vlc", "mplayer", "mpv", "wmplayer", "quicktime", "potplayer", "gplayer", "realplayer", "movies & tv"
    ]

    # Check for the installed media players by searching for known executables
    for player in potential_players:
        try:
            # Try running the player to see if it's installed
            subprocess.run([player, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            players.append(player)  # Add to the list if found
        except FileNotFoundError:
            continue  # Skip if the executable is not found

    if not players:
        messagebox.showerror("No Media Players", "No compatible media players were found on your system.")

    return players


def open_video_with_player(video_path, player_name):
    """Open the video using the selected media player."""
    try:
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"The video file {video_path} could not be found.")
        
        if player_name.lower() == "vlc":
            subprocess.run([r"C:\Program Files\VideoLAN\VLC\vlc.exe", video_path])
        elif player_name.lower() == "wmplayer":
            subprocess.run([r"C:\Program Files (x86)\Windows Media Player\wmplayer.exe", video_path])
        elif player_name.lower() == "movies & tv":
            subprocess.run([r"C:\Program Files\Microsoft Movies & TV\Video.UI.exe", video_path])
        else:
            # Try the general method if the player path is known
            subprocess.run([player_name, video_path])

        print(f"Successfully opened {video_path} with {player_name}.")
    except Exception as e:
        messagebox.showerror("Error", f"Error opening video with {player_name}: {e}")


def open_media_player_selection(video_path):
    """Open a window for the user to select a media player."""
    # Get list of installed media players
    media_players = get_installed_media_players()

    if not media_players:
        messagebox.showerror("No Players", "No media players were detected.")
        return

    media_player_window = tk.Toplevel()
    media_player_window.title("Select Media Player")

    # List box to display the available players
    listbox = tk.Listbox(media_player_window)
    for player in media_players:
        listbox.insert(tk.END, player.capitalize())
    listbox.pack(pady=10)

    def play_video():
        selected_player = listbox.get(tk.ACTIVE)
        if selected_player:
            open_video_with_player(video_path, selected_player)
            media_player_window.destroy()
        else:
            messagebox.showerror("Error", "Please select a media player.")

    # Button to play video with selected player
    tk.Button(media_player_window, text="Play", command=play_video).pack(pady=5)

    # Button to close the selection window
    tk.Button(media_player_window, text="Cancel", command=media_player_window.destroy).pack(pady=5)
