# Group-Project-Smart-Phone
A OOPs based Project that will implement all functionality of working Smart Phone

# 📱 Vracks Team Virtual Phone - Python Mobile Simulation App

A powerful, GUI-based mobile phone simulation application developed in Python using Tkinter. This desktop-based virtual phone integrates multimedia, AI-powered utilities, communication tools, and a file system — emulating core functionalities of a smartphone.

---

## 🏗️ Project Structure

This app is designed as a **monolithic single-file application** (`server.py`) using class-based modular functions under the `Mobile_Phone` class. It also integrates multi-threading and file I/O to simulate a responsive, dynamic phone environment.


## Some Screenshots

![image](https://github.com/user-attachments/assets/e22c6c59-e910-41b2-82f2-3920dd6889ba)
![image](https://github.com/user-attachments/assets/359caa7a-12b7-4944-a0cd-1a47554a7c86)
![image](https://github.com/user-attachments/assets/cfafd8f5-0286-4438-9736-25f7e2f762c2)
![image](https://github.com/user-attachments/assets/72b17bda-0d96-4a65-9c91-a42b418549d4)
![image](https://github.com/user-attachments/assets/6cdc37e2-0665-4f92-8bf5-6e1f3836aaaf)
![image](https://github.com/user-attachments/assets/b5ce060b-fce4-4e14-b1b9-68d75ed31359)
![image](https://github.com/user-attachments/assets/2499ac6c-bea2-47a4-af99-6e8dabb7ddaa)
![image](https://github.com/user-attachments/assets/26779775-a52b-4762-a3e6-d060b62d0d26)
![image](https://github.com/user-attachments/assets/d4d7c6f5-ad2c-4d38-828b-232ee1e996c6)


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


