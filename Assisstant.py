import os
import platform
import difflib
import webbrowser
import urllib.parse
import random

# Base media player class
class MediaPlayer:
    def __init__(self, folder_path, valid_extensions):
        self.folder_path = folder_path
        self.valid_extensions = valid_extensions
        self.files = self._scan_files()

    def _scan_files(self):
        if not os.path.exists(self.folder_path):
            print(f"Folder not found: {self.folder_path}")
            return []
        return [
            f for f in os.listdir(self.folder_path)
            if os.path.isfile(os.path.join(self.folder_path, f)) and
            os.path.splitext(f)[1].lower() in self.valid_extensions
        ]
    
    # To access sub folders also
    '''
    def _scan_files(self):
        found_files = []
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                if os.path.splitext(file)[1].lower() in self.valid_extensions:
                    full_path = os.path.join(root, file)
                    found_files.append(os.path.relpath(full_path, self.folder_path))
        return found_files
    '''

    def list_files(self):
        if not self.files:
            print("No media files found.")
            return
        print("\nAvailable Files:")
        for index, file in enumerate(self.files, 1):
            print(f"   {index}. {file}")

    def suggest_filename(self, user_input):
        matches = difflib.get_close_matches(user_input, self.files, n=1, cutoff=0.4)
        return matches[0] if matches else None

    def open_file(self, filename):
        full_path = os.path.abspath(os.path.join(self.folder_path, filename))
        if not os.path.exists(full_path):
            print("File does not exist.")
            return
        system = platform.system()
        print(f"Opening: {full_path}")
        if system == "Windows":
            os.startfile(full_path)
        elif system == "Darwin":
            os.system(f"open '{full_path}'")
        else:
            os.system(f"xdg-open '{full_path}'")

# Music Player
class MusicPlayer(MediaPlayer):
    def __init__(self, folder_path):
        super().__init__(folder_path, ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'])

    def play_music(self):
        self.list_files()
        if not self.files:
            return
        
        user_input = input("\nEnter song name (partial/full) or type 'shuffle' to shuffle songs: ").strip()

        if user_input == "shuffle":
            random_song = random.choice(self.files)
            print(f"Shuffled: {random_song}")
            self.open_file(random_song)
            return
    
        match = self.suggest_filename(user_input)
        if match:
            print(f"Best match: {match}")
            self.open_file(match)
        else:
            print("No close match found.")

# Video Player
class VideoPlayer(MediaPlayer):
    def __init__(self, folder_path):
        super().__init__(folder_path, ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.webm'])

    def play_video(self):
        self.list_files()
        if not self.files:
            return
        user_input = input("\nEnter video name (partial/full): ").strip()
        match = self.suggest_filename(user_input)
        if match:
            print(f"Best match: {match}")
            self.open_file(match)
        else:
            print("No close match found.")

# YouTube Search
class YouTube:
    def search(self):
        query = input("\n What do you want to search on YouTube? ").strip()
        if not query:
            print("Empty search is not allowed.")
            return
        search_url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
        print(f"Opening YouTube search for: {query}")
        webbrowser.open(search_url)

# Assistant Menu
def match_command(text, keywords):
    text = text.lower()
    for keyword in keywords:
        return any(keyword in text for keyword in keywords)


def main_assistant():
    # Replace with actual folders
    music_folder = "D:/Music"
    video_folder = "D:/#ANIME/Fullmetal alchemist"

    music_player = MusicPlayer(music_folder)
    video_player = VideoPlayer(video_folder)
    youtube = YouTube()

    print("Welcome to Smart Assistant!")

    while True:
        user_input = input("What do you want to do (or type 'exit')? ").strip().lower()
        print(f"[DEBUG] You entered: {user_input}")

        if user_input in ("exit", "quit", "close"):
            print(" Exiting Smart Assistant.")
            break

        elif match_command(user_input, ["music", "audio", "songs", "audio player", "music player"]):
            music_player.play_music()

        elif match_command(user_input, ["video", "videos", "movie", "film", "video player"]):
            video_player.play_video()

        elif match_command(user_input, ["youtube", "yt", "search youtube"]):
            youtube.search()

        elif "player" in user_input:
            follow_up = input("Do you want music or video player? ").strip().lower()
            if "music" in follow_up or "audio" in follow_up:
                music_player.play_music()
            elif "video" in follow_up:
                video_player.play_video()
            else:
                print("Didn't understand. Please say music or video.")

        else:
            print("I didn't understand that. Try something like 'music', 'video', or 'YouTube'.")

# Run the Assistant
if __name__ == "__main__":
    main_assistant()
