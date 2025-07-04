# Group Project - Smart Assistant in Python

This project is a **terminal-based smart assistant** that simulates basic smartphone functionalities using Python.

It allows you to:
- 🎧 Play local music files (with filename suggestions)
- 🎬 Play local video files (with filename suggestions)
- 🔍 Search anything on YouTube directly from your terminal


## 📦 Features

✅ Natural language input like:
- `open music`, `audio player`, `songs`
- `video`, `movie`, `video player`
- `youtube`, `search YouTube`

✅ File name **autocompletion** — type partial names like `believer` or `home` and it finds the right file

✅ Auto-opens files in your system’s **default media player**

✅ Cross-platform: Windows, Linux, macOS


## 🛠 Requirements

- Python 3.x
- No additional packages needed (uses built-in `os`, `platform`, `webbrowser`, etc.)


## 📁 Folder Setup

Before running the assistant, create the following folder structure inside your project directory:

project-root/
├── Smart_assistant.ipynb # 🧠 Main Python assistant file (Jupyter Notebook)
├── README.md # 📘 This documentation
├── Music/ # 🎧 Store your audio files here (e.g., .mp3, .wav, etc.)
  └── .gitkeep # Placeholder to keep folder tracked on GitHub
├── Videos/ # 🎬 Store your video files here (e.g., .mp4, .mkv, etc.)
  └── .gitkeep

> Note: The `.gitkeep` files are optional empty files that ensure these folders remain in the GitHub repo even if they contain no media yet.


Place your music files (like `song1.mp3`, `lofi.wav`, etc.) in the **`Music/`** folder, and your video files (like `movie.mp4`, `clip.mkv`, etc.) in the **`Videos/`** folder.

If no media is found in the specified folders, the assistant will say:  
No media files found.

You can customize the folder paths inside `Smart_assistant.ipynb` if you wish to use a different structure.
