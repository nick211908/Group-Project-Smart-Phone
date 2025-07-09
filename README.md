# Group-Project-Smart-Phone
A OOPs based Project that will implement all functionality of working Smart Phone

# 📱 Vracks Team Virtual Phone - Python Mobile Simulation App

A powerful, GUI-based mobile phone simulation application developed in Python using Tkinter. This desktop-based virtual phone integrates multimedia, AI-powered utilities, communication tools, and a file system — emulating core functionalities of a smartphone.

---

## 🏗️ Project Structure

This app is designed as a **monolithic single-file application** (`server.py`) using class-based modular functions under the `Mobile_Phone` class. It also integrates multi-threading and file I/O to simulate a responsive, dynamic phone environment.


## Some Screenshots

![image](https://github.com/user-attachments/assets/adb3fbd2-d9ff-4b77-a714-212b8d82f73a)
![image](https://github.com/user-attachments/assets/e52536e1-84bf-4b8d-aff9-e13833857b9e)
![image](https://github.com/user-attachments/assets/92caa4c9-5010-479b-9516-e55c901f4008)
![image](https://github.com/user-attachments/assets/0a63195d-3267-4240-a0b6-e7e91f6368c0)
![image](https://github.com/user-attachments/assets/e85199a4-a183-4a5c-ad69-ccd4c51f17b0)
![image](https://github.com/user-attachments/assets/fd3835c9-dca4-40ab-a287-04fa8d9bcc7d)
![image](https://github.com/user-attachments/assets/5f00c902-3d9c-452b-acf2-67abbf672e06)
![image](https://github.com/user-attachments/assets/5a7e2fb4-00cc-494a-9466-691fe919e712)

📁 Mobile_Phone_Project/
├── server.py # Main application logic and GUI
├── 📁 data/ # Persistent storage (pickle-based)
│ └── mobile_data.bin # User data and app storage
├── 📁 media/ # All user-generated media
│ └── 📁 images/ # Saved snapshots
├── 📁 templates/ (if used) # [Optional: for Flask extension]
└── 📄 README.md # This file


---

## 🧠 Features and Modules

The app is split into the following major segments:

### 1. 🌐 Global Configuration
- Imports essential libraries: `cv2`, `tkinter`, `PIL`, `smtplib`, `speech_recognition`, `pyttsx3`, `webbrowser`, etc.
- Sets global constants for theme colors, ADB path, and storage files.
- Voice engine and command recognition support.

---

### 2. 📦 Mobile_Phone Class (Main App Controller)

Handles:
- Persistent file-based storage using `pickle`.
- Modular app logic for each functionality.
- Stores all app data under `self.storage`.

---

### 3. 📇 Contacts App
- `save_contact_gui()`: Save new contacts via GUI.
- `view_contacts_gui()`: Display all saved contacts.
- `make_call_gui()`: Use ADB to simulate calls to contacts or numbers.

---

### 4. 🤖 AI Camera App
- `ai_camera_capture_palm()`: Uses OpenCV to click images when palm is detected.
- `manual_capture()`: Takes one-click snapshots.
- `open_gallery()`: Displays captured images in a scrollable gallery view.

---

### 5. 📽️ Media Player & Scanner
- `scan_media_files()`: Scans and indexes all `.mp3`, `.mp4`, `.wav`, etc. in `/media`.
- `play_media_gui()`: GUI to play selected media.
- Supports OS-level opening using `os.startfile()` or `xdg-open`.

---

### 6. 📄 PDF Viewer
- `open_pdf_viewer()`: Opens multi-page PDF using `PyMuPDF` with scrollable Tkinter GUI.

---

### 7. ✉️ AI Email Sender
- `launch_email_gui()`: Compose and send Gmail using Gemini AI to generate personalized body content.
- Attachments supported.
- History and last email saved in JSON/text files.

---

### 8. 🌍 URL Launcher
- `launch_url_opener()`: Opens any URL in browser (tab/window mode).
- Dark mode toggle and URL history feature.

---

### 9. 🎬 YouTube + Chrome Launcher
- Opens a predefined YouTube search (`"Python programming"`) in MS Edge.
- Can launch Google Chrome if installed.

---

### 10. ⏰ Alarm & Reminders
- `launch_alarm_gui()`: Set reminders in "HH:MM ➜ Note" format.
- `start_alarm_checker()`: Background thread checks every 30s and uses voice + desktop notifications.

---

### 11. 📞 WhatsApp Launcher
- Opens WhatsApp (if available) using `os.system("start whatsapp:")`.

---

## 🎛️ GUI Layout Overview

Tkinter GUI layout is grouped logically:

- **Camera Apps**
- **Media & Files**
- **Phone & Contacts**
- **Communication Tools**
- **Utility Apps (Alarms, WhatsApp, YouTube)**

---

## 💾 Storage & Persistence

- `./data/mobile_data.bin` → All contacts, media history, alarms stored using `pickle`.
- `email_history.json` → All Gemini-generated emails.
- `last_email.txt` → Stores last composed email.
- `url_history.json` → Stores last opened URL.

---

## 🛠️ Dependencies

Install via:

```bash
pip install opencv-python pyttsx3 pillow PyMuPDF google-generativeai speechrecognition pywebview plyer


