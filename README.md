# Group-Project-Smart-Phone
A OOPs based Project that will implement all functionality of working Smart Phone

# 📱 Vracks's Virtual Phone (Tkinter + ADB + AI + Voice Assistant)

Welcome to **Vracks's Virtual Phone** — a smart mobile simulation app built using Python, Tkinter GUI, ADB shell, OpenCV AI camera, and Gemini-powered email composer. This virtual phone system mimics a smartphone experience with real desktop interactions.

---

## 🚀 Features

### 🎙️ AI Voice Assistant
- Activate with **voice commands**
- Supports commands like:
  - "Open gallery", "Take palm photo", "Open PDF", "Play music", etc.

### 📷 AI Camera
- **Palm detection** to auto-click photos using OpenCV
- **Manual capture** with instant webcam shot
- 📁 Saves all images to `./media/images/`

### 📇 Contacts & Calling (via ADB)
- Save/view contacts locally
- Call contact by name or number using ADB:
  - `adb shell am start -a android.intent.action.CALL -d tel:{number}`

### 🎵 Media & Music Player
- Scan and play local `.mp3`, `.wav`, `.mp4`, `.mkv` files
- Smart **search** and **shuffle play**
- Interactive GUI list selection

### 🖼️ Image Gallery
- Dynamic thumbnail-based gallery view
- Click to open image in default viewer
- Loads images from `./media/images/`

### 📄 PDF Viewer
- Select and open PDF in a GUI within a chrome pdf reader
- Supports file dialog selection

### ✉️ Email Generator (Gemini AI)
- Launch Gmail from the app
- Auto-generate email with Gemini:
  - Input: name, topic, tone → Output: formatted email body
- Saves history in `email_history.json`

### 🌐 URL Launcher
- Opens any URL in **tab/window**
- Toggleable **dark mode UI**
- Saves last used URL in `url_history.json`

### 🧠 AI + Voice
- Uses:
  - `pyttsx3` for TTS
  - `speech_recognition` for command detection
  - Google Gemini for email writing

### 📦 Utility Apps
- Open system apps with `os.system()`:
  - WhatsApp (`start whatsapp:`)
  - Camera (`microsoft.windows.camera:`)
  - Calculator (`start calc`)
  - Calendar (`start outlookcal:`)
  - YouTube / Instagram in browser

---

## 🧱 Project Structure

├── media/

│ ├── images/ # AI Camera and Manual Captures

│ ├── (music/videos) # Media scanned and played

├── data/

│ ├── mobile_data.bin # Contact & Media Storage (Pickle)

├── server.py # 📱 Main Script

---

## 🖼️ Screenshots

> 📌 _Add screenshots here for each app window._

| Feature            | Screenshot Preview                      |
|--------------------|------------------------------------------|
| **Main GUI Layout** | (<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/4acae14d-4750-482f-b6fc-ece934c4c4e9" />) |
| **Palm Detection**  | (<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c55f2134-7343-4fab-8a50-ac6bda70bd93" />) |
| **Gallery Viewer**  | (<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/eebcf817-ed29-4cea-afc7-85aa3ee5c77f" />)  |
| **Music Player**    | (<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/60bb9624-cb9d-4504-be50-9a1b3154d90d" />) |
| **Media Player**    | (<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/68272cf4-cda3-41c7-a5d1-89dd07b64475" />) |
| **Contact Manager** | (<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3c1d85be-5b6a-49d4-87bf-df59d360cbdc" />) |
| **URL Launcher**    | (<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a4ccff48-7af8-4fc3-a9ce-e86c5e984f21" />) |

📝 _Place all screenshots in the `./screenshots/` folder in your project root._

---

## 🎥 Recordings

> 📌 _Embed or link demo videos here (YouTube, Drive, etc.)._

- 🎬 [**Demo - Full Virtual Phone Experience**](https://screenrec.com/share/R8snTIfrm7)

💡 _For best viewing, host on YouTube or Google Drive with public access._

---
---

## 🛠️ Requirements

Install required libraries via `pip`:

```bash
pip install opencv-python pillow pyttsx3 plyer SpeechRecognition google-generativeai PyMuPDF
```

✅ **Ensure ADB is installed** and added to your system `PATH` for call functionality to work.

---

## 🧠 Technologies Used

- 🐍 **Python 3.8+**
- 🖼️ **Tkinter GUI** for the mobile interface
- 🧠 **OpenCV** for palm detection via webcam
- 📄 **PyMuPDF** for PDF file rendering
- ✨ **Google Gemini API** for AI-powered email composition
- 🔊 **Pyttsx3** for text-to-speech responses
- 🗣️ **SpeechRecognition** for capturing voice commands
- 📞 **ADB (Android Debug Bridge)** to simulate calling from PC

---

## 🧑‍💻 Author

Made with ❤️ by **Vracks's Team**

---

## 📌 Note

This app is built for **desktop simulation only**.  
Ensure your system has:

- A webcam for AI Camera features
- Internet access for Gemini API
- ADB configured for call simulation
- A default browser to open PDFs, URLs, etc.

---

## 🧪 To Run

```bash
python vracks_virtual_phone.py
```

Make sure all required folders are auto-created:

```
./media/
├── images/        # Camera captures
./data/            # Stores contacts and media info
```

---

## ✨ Contribute

PRs and ideas are welcome! Some planned improvements include:

- 📬 Gemini-powered Email **sending** via SMTP
- 🔍 AI-based Smart Search
- ⚙️ Dynamic App Configuration System
- 🌈 Custom themes & sound effects

---

## 📄 License

Licensed under the **MIT License** — free for personal and educational use.

---


