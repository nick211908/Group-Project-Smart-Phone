# ================================================
# 1. Global Setup & Configurations
# ================================================
import io
from logging import root
import os
import subprocess
import webbrowser
import shutil
import pickle
import cv2
import time
import difflib
import platform
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Entry, Frame, Label, Button, Toplevel, StringVar, ttk
from datetime import datetime
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import json
import smtplib
from email.message import EmailMessage
import threading
import pyttsx3
import webbrowser
import webview
import speech_recognition as sr
import google.generativeai as genai
from plyer import notification



HISTORY_FILE = "email_history.json"
LAST_EMAIL_FILE = "last_email.txt"
URL_HISTORY_FILE = "url_history.json"
DARK_MODE = True
BG_COLOR = "#669BBC" if DARK_MODE else "#f0f4f8"
FG_COLOR = "#ecf0f1" if DARK_MODE else "#2c3e50"
ENTRY_BG = "#34495e" if DARK_MODE else "white"
BTN_COLOR = "#780000"
adb_path = "adb"
capture_mode = "quick"
DEVICE_ID = None

engine = pyttsx3.init()

def speak(text):
    print(f"[Voice]: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_for_keyword():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening... say your command.")
        print("🎙️ Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"[Detected]: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand.")
    except sr.RequestError:
        speak("Speech service is down.")
    return ""

def match_command(input_text, commands):
    return any(word in input_text for word in commands)

# ================================================
# 2. Mobile_Phone Class and Data Handling
# ================================================

class Mobile_Phone:
    def __init__(self, user):
        self.user = user
        self.storage_path = "./data/mobile_data.bin"
        self.storage = self.load_data(self.storage_path)
        self.push_data(self.storage_path, "user", self.user)

    def load_data(self, file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, "wb") as f:
                pickle.dump({}, f)
            return {}
        try:
            with open(file_path, "rb") as f:
                return pickle.load(f)
        except EOFError:
            return {}

    def push_data(self, file_path, key, new_value):
        data = self.load_data(file_path)
        data[key] = new_value
        with open(file_path, "wb") as f:
            pickle.dump(data, f)
        print(f"✅ Updated '{key}' in '{file_path}'")

# ================================================
# 3. Contacts App
# ================================================

    def save_contact(self, name, number):
        if not name or not number.isdigit():
            return ("error", "Invalid input")
        contacts = self.storage.get("contacts", [])
        for n, _ in contacts:
            if n.lower() == name.lower():
                return ("duplicate", f"Contact '{name}' already exists.")
        contacts.append((name, number))
        self.storage["contacts"] = contacts
        self.push_data(self.storage_path, "contacts", contacts)
        return ("success", f"Contact '{name}' saved.")
    
    def save_contact_gui(self):
        def save():
            name = name_entry.get()
            number = number_entry.get()
            status, msg = self.save_contact(name, number)
            tk.messagebox.showinfo("Save Status", msg)

        win = tk.Toplevel()
        win.title("➕ Save Contact")

        tk.Label(win, text="Name:").pack(pady=2)
        name_entry = tk.Entry(win)
        name_entry.pack(pady=2)

        tk.Label(win, text="Phone Number:").pack(pady=2)
        number_entry = tk.Entry(win)
        number_entry.pack(pady=2)

        tk.Button(win, text="💾 Save", command=save).pack(pady=10)


    def get_contacts(self):
        return self.storage.get("contacts", [])
    
    def view_contacts_gui(self):
        contacts = self.get_contacts()
        win = tk.Toplevel()
        win.title("📇 Contact List")

        if not contacts:
            tk.Label(win, text="No contacts found.", font=("Helvetica", 12)).pack(padx=10, pady=10)
            return

        for name, number in contacts:
            contact_str = f"{name}: {number}"
            tk.Label(win, text=contact_str, font=("Helvetica", 12)).pack(padx=10, pady=5)


    def make_call(self, name_or_number):
        contacts = self.get_contacts()
        number = name_or_number if name_or_number.isdigit() else             next((n for n_name, n in contacts if n_name.lower() == name_or_number.lower()), None)
        if number is None:
            return ("error", f"No contact found for '{name_or_number}'")
        cmd = f'adb shell am start -a android.intent.action.CALL -d tel:{number}'
        result = os.system(cmd)
        return ("success", f"Calling {number}...") if result == 0 else ("error", "Failed to initiate call.")

    def make_call_gui(self):
        def call():
            name_or_number = entry.get()
            result, msg = self.make_call(name_or_number)
            tk.messagebox.showinfo("Call Status", msg)

        win = tk.Toplevel()
        win.title("📞 Make a Call")

        tk.Label(win, text="Name or Phone Number:").pack(pady=5)
        entry = tk.Entry(win)
        entry.pack(pady=5)

        tk.Button(win, text="📲 Call", command=call).pack(pady=10)


# ================================================
# 4. AI Camera App
# ================================================

    def ai_camera_capture_palm(self, save_dir="./media/images"):
        os.makedirs(save_dir, exist_ok=True)
        cap = cv2.VideoCapture(0)
        cooldown, last_click_time = 5, 0
        print("🖐️ Show palm to capture")
        while True:
            ret, frame = cap.read()
            if not ret: break
            roi = frame[100:400, 100:400]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (35, 35), 0)
            _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                cnt = max(contours, key=cv2.contourArea)
                hull = cv2.convexHull(cnt, returnPoints=False)
                if hull is not None and len(hull) > 3:
                    defects = cv2.convexityDefects(cnt, hull)
                    if defects is not None and len(defects) >= 4:
                        now = time.time()
                        if now - last_click_time > cooldown:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            path = os.path.join(save_dir, f"palm_{timestamp}.png")
                            cv2.imwrite(path, frame)
                            print(f"📸 Saved {path}")
                            last_click_time = now
            cv2.rectangle(frame, (100, 100), (400, 400), (0, 255, 0), 2)
            cv2.imshow("Palm Capture", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break
        cap.release()
        cv2.destroyAllWindows()

    def manual_capture(self, save_dir="./media/images"):
        os.makedirs(save_dir, exist_ok=True)
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(save_dir, f"manual_{timestamp}.png")
            cv2.imwrite(path, frame)
            print(f"📸 Manual capture saved to {path}")
        cap.release()


    def scan_media_files(self, folder="./media", exts={".mp3", ".mp4", ".wav", ".mkv"}):
        found = []
        for root_dir, _, files in os.walk(folder):
            for file in files:
                if os.path.splitext(file)[1].lower() in exts:
                    found.append(os.path.relpath(os.path.join(root_dir, file), folder))
        # Do NOT save in binary — only in memory
        self.storage.setdefault("media_player", {"available_files": [], "history": [], "last_played": None})
        self.storage["media_player"]["available_files"] = found
        return found


    
    def play_media(self, query, folder="./media"):
        files = self.storage.get("media_player", {}).get("available_files", [])
        match = difflib.get_close_matches(query, files, n=1, cutoff=0.4)
        if not match:
            return ("error", f"No media file matching '{query}'")
        file = match[0]
        full = os.path.join(folder, file)
        try:
            if platform.system() == "Windows":
                os.startfile(full)
            elif platform.system() == "Darwin":
                os.system(f"open '{full}'")
            else:
                os.system(f"xdg-open '{full}'")
        except Exception as e:
            return ("error", str(e))
        self.storage["media_player"]["history"].append({"file": file, "time": str(datetime.now())})
        self.push_data(self.storage_path, "media_player", self.storage["media_player"])
        return ("success", f"Playing '{file}'")
    
    def play_media_gui(self, folder="./media"):
        files = self.storage.get("media_player", {}).get("available_files", [])
        if not files:
            tk.messagebox.showinfo("No Files", "No media files found. Please scan media first.")
            return

        def play_selected():
            selection = listbox.curselection()
            if not selection:
                tk.messagebox.showwarning("No Selection", "Select a media file to play.")
                return
            selected_file = files[selection[0]]
            self.play_media(selected_file, folder)

        win = tk.Toplevel()
        win.title("🎬 Select Media to Play")

        listbox = tk.Listbox(win, width=60, height=20, font=("Helvetica", 11))
        listbox.pack(padx=10, pady=10)

        for f in files:
            listbox.insert(tk.END, f)

        tk.Button(win, text="▶️ Play", command=play_selected, bg="green", fg="white").pack(pady=10)


    def open_gallery(self, folder="./media/images"):
        win = tk.Toplevel()
        win.title("📸 Image Gallery")
        for file in os.listdir(folder):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    img_path = os.path.join(folder, file)
                    img = Image.open(img_path)
                    img = img.resize((200, 200))
                    tk_img = ImageTk.PhotoImage(img)
                    label = tk.Label(win, image=tk_img)
                    label.image = tk_img
                    label.pack(padx=5, pady=5)
                except Exception as e:
                    print(f"⚠️ Skipped corrupted image '{file}': {e}")


    def open_pdf_viewer(self, pdf_path=None):
        win = tk.Toplevel()
        win.title("📄 PDF Viewer")
        win.geometry("900x700")

        if not pdf_path:
            pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not pdf_path:
            return

        try:
            doc = fitz.open(pdf_path)

            container = tk.Frame(win)
            canvas = tk.Canvas(container, width=850, bg="white")
            scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
            scroll_frame = tk.Frame(canvas)

            scroll_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            container.pack(fill="both", expand=True)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            for i, page in enumerate(doc):
                pix = page.get_pixmap(dpi=150)
                image_data = pix.tobytes("png")
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((800, int(800 * image.height / image.width)), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                label = tk.Label(scroll_frame, image=photo, bg="white")
                label.image = photo  # Keep a reference
                label.pack(pady=10)

            doc.close()

        except Exception as e:
            messagebox.showerror("PDF Error", f"Could not display PDF:\n{e}")




    def launch_email_gui(self):
        def send_email():
            name = name_entry.get()
            to_email = to_email_entry.get()
            topic = topic_entry.get()
            from_email = your_email_entry.get()
            app_password = app_pass_entry.get()
            gemini_key = gemini_key_entry.get()
            tone = tone_var.get()
            subject = f"Regarding {topic.title()}"
            attachment_path = attachment_label['text']

            if not all([name, to_email, topic, from_email, app_password, gemini_key]):
                messagebox.showerror("Error", "All fields except attachment are required.")
                return

            self.setup_gemini(gemini_key)
            body = self.generate_gemini_message(name, topic, tone)

            if body.startswith("Error:"):
                messagebox.showerror("Gemini Error", body)
                return

            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = to_email
            msg.set_content(body)

            if attachment_path and os.path.isfile(attachment_path):
                try:
                    with open(attachment_path, 'rb') as f:
                        file_data = f.read()
                        file_name = os.path.basename(attachment_path)
                        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
                except Exception as e:
                    messagebox.showerror("Attachment Error", f"Failed to attach file: {e}")
                    return

            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(from_email, app_password)
                    smtp.send_message(msg)
                self.save_to_history(name, to_email, topic, tone, body)
                self.export_last_email(subject, body)
                messagebox.showinfo("Success", "✅ Email sent successfully!")
            except Exception as e:
                messagebox.showerror("SMTP Error", f"❌ Failed to send email: {e}")

        def choose_file():
            file_path = filedialog.askopenfilename()
            if file_path:
                attachment_label.config(text=file_path)

        email_root = Toplevel()
        email_root.title("Email Sender")
        email_root.geometry("650x600")
        email_root.configure(bg=BG_COLOR)

        Label(email_root, text="Email Sender", font=("Helvetica", 20, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=15)

        def field(label_text, is_pass=False):
            frame = Frame(email_root, bg=BG_COLOR)
            frame.pack(pady=5)
            Label(frame, text=label_text, font=("Helvetica", 12), bg=BG_COLOR, fg=FG_COLOR).pack(anchor="w")
            entry = Entry(frame, width=50, font=("Helvetica", 11), bg=ENTRY_BG, fg=FG_COLOR, show="*" if is_pass else "")
            entry.pack()
            return entry

        name_entry = field("Recipient Name:")
        to_email_entry = field("Recipient Email:")
        topic_entry = field("Email Topic:")
        your_email_entry = field("Your Gmail:")
        app_pass_entry = field("Gmail Password:", is_pass=True)
        gemini_key_entry = field("API Key:", is_pass=True)

        tone_var = StringVar(value="friendly")
        tone_frame = Frame(email_root, bg=BG_COLOR)
        tone_frame.pack(pady=5)
        Label(tone_frame, text="Select Tone:", font=("Helvetica", 12), bg=BG_COLOR, fg=FG_COLOR).pack(anchor="w")
        ttk.Combobox(tone_frame, textvariable=tone_var, values=["friendly", "formal", "flirty", "funny", "strict"], width=47).pack()

        Button(email_root, text="📎 Choose Attachment", command=choose_file, bg="#3498db", fg="white", font=("Helvetica", 10)).pack(pady=5)
        attachment_label = Label(email_root, text="", bg=BG_COLOR, fg="#bdc3c7", font=("Helvetica", 9))
        attachment_label.pack()

        Button(email_root, text="🚀 Send Email", command=send_email, bg=BTN_COLOR, fg="white", font=("Helvetica", 13, "bold"), width=30).pack(pady=20)



    def setup_gemini(self, api_key):
        genai.configure(api_key=api_key)

    def generate_gemini_message(self, name, topic, tone):
        prompt = f"Write a {tone.lower()} email to {name} about '{topic}'. Sign it as 'Your Automated Assistant'."
        try:
            model = genai.GenerativeModel(model_name="gemini-pro")
            response = model.generate_content([prompt])
            return response.text.strip()
        except Exception as e:
            return f"Error: {e}"

    def save_to_history(self, name, to_email, topic, tone, message):
        record = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "to": to_email,
            "name": name,
            "topic": topic,
            "tone": tone,
            "message": message
        }
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        history.append(record)
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)

    def export_last_email(self, subject, body):
        with open(LAST_EMAIL_FILE, "w") as f:
            f.write(f"Subject: {subject}\n\n{body}")



    def launch_url_opener(self):
        def open_url():
            url = validate_url(url_entry.get())
            mode = mode_var.get()
            if not url or url.isspace():
                messagebox.showerror("Error", "Please enter a valid URL.")
                return
            save_url(url)
            try:
                if mode == "tab":
                    webbrowser.open_new_tab(url)
                elif mode == "window":
                    webbrowser.open_new(url)
                else:
                    messagebox.showwarning("Warning", "Please select how to open the URL.")
                    return
                messagebox.showinfo("Opened", f"Successfully opened:\n{url}")
            except Exception as e:
                messagebox.showerror("Failed", f"Could not open URL:\n{e}")

        def toggle_dark_mode():
            global DARK_MODE
            DARK_MODE = not DARK_MODE
            bg = "#222" if DARK_MODE else "#f0f0f0"
            fg = "#fff" if DARK_MODE else "#000"
            root.configure(bg=bg)
            for widget in root.winfo_children():
                widget.configure(bg=bg, fg=fg)
            dark_button.configure(text="☀ Light Mode" if DARK_MODE else "🌙 Dark Mode")

        root = tk.Toplevel()
        root.title("🌐 Open Website")
        root.geometry("420x280")

        url_label = tk.Label(root, text="Enter Website URL:", font=('Arial', 12))
        url_label.pack(pady=5)
        url_entry = tk.Entry(root, width=50)
        url_entry.pack(pady=5)
        url_entry.insert(0, load_last_url())

        mode_var = tk.StringVar()
        tk.Label(root, text="Open in:", font=('Arial', 11)).pack(pady=5)
        tk.Radiobutton(root, text="New Tab", variable=mode_var, value="tab").pack()
        tk.Radiobutton(root, text="New Window", variable=mode_var, value="window").pack()
        tk.Button(root, text="Open URL", command=open_url, bg="green", fg="white", font=('Arial', 12)).pack(pady=10)
        dark_button = tk.Button(root, text="🌙 Dark Mode", command=toggle_dark_mode, font=('Arial', 10))
        dark_button.pack()

    def open_youtube_brave(self):
        try:
            print("Attempting to search for 'Python programming' on YouTube...")
            os.system("start msedge https://www.youtube.com/results?search_query=Python+programming")
            print("Command sent to search for 'Python programming' on YouTube.")
        except Exception as e:
            print(f"Failed to search on YouTube: {e}")

    def open_chrome():
    # Try to find Chrome path
        chrome_path = None
        if os.name == 'nt':  # Windows
            chrome_path = shutil.which("chrome") or shutil.which("google-chrome")
            if not chrome_path:
                chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

        if os.path.exists(chrome_path):
            subprocess.Popen([chrome_path])
            print("Google Chrome is now open.")
        else:
            print("⚠️ Chrome not found.")

    def launch_alarm_gui(self):
        def add_alarm():
            time_val = time_entry.get()
            note_val = note_entry.get()
            if not time_val or not note_val:
                messagebox.showerror("Error", "Please fill both time and note.")
                return
            alarms = self.storage.get("alarm", {})
            alarms[time_val] = note_val
            self.storage["alarm"] = alarms
            self.push_data(self.storage_path, "alarm", alarms)
            messagebox.showinfo("Success", f"Alarm for {time_val} saved!")

        def view_alarms():
            win = Toplevel()
            win.title("⏰ Saved Alarms")
            alarms = self.storage.get("alarm", {})
            if not alarms:
                tk.Label(win, text="No alarms set.", font=("Helvetica", 12)).pack(padx=10, pady=10)
            else:
                for time_str, msg in alarms.items():
                    tk.Label(win, text=f"{time_str} ➜ {msg}", font=("Helvetica", 12)).pack(pady=3)

        win = Toplevel()
        win.title("⏰ Alarm App")
        win.geometry("350x300")
        win.configure(bg=BG_COLOR)

        tk.Label(win, text="Set New Alarm", font=("Helvetica", 14, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)

        frame = Frame(win, bg=BG_COLOR)
        frame.pack(pady=5)
        tk.Label(frame, text="Time (HH:MM):", font=("Helvetica", 11), bg=BG_COLOR, fg=FG_COLOR).pack()
        time_entry = tk.Entry(frame, font=("Helvetica", 11))
        time_entry.pack()

        tk.Label(frame, text="Note/Reminder:", font=("Helvetica", 11), bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        note_entry = tk.Entry(frame, font=("Helvetica", 11))
        note_entry.pack()

        tk.Button(win, text="➕ Add Alarm", command=add_alarm, bg="#198754", fg="white").pack(pady=10)
        tk.Button(win, text="📋 View Alarms", command=view_alarms, bg="#0d6efd", fg="white").pack()

    def start_alarm_checker(self):

        def check_alarms():
            while True:
                now = datetime.now().strftime("%H:%M")
                alarms = self.storage.get("alarm", {})
                if now in alarms:
                    note = alarms[now]
                    for _ in range(3):  # Repeat 3 times
                        speak(f"Alarm! {note}")
                        notification.notify(
                            title="⏰ Alarm Alert!",
                            message=f"{now} - {note}",
                            timeout=5
                        )
                        time.sleep(10)  # Wait 10 sec between announcements
                    # Remove triggered alarm to avoid infinite repeats
                    del alarms[now]
                    self.storage["alarm"] = alarms
                    self.push_data(self.storage_path, "alarm", alarms)
                time.sleep(30)  # Check every 30 seconds

        threading.Thread(target=check_alarms, daemon=True).start()

    def open_whatsapp(self):
        try:
            print("Attempting to open WhatsApp...")
            os.system("start whatsapp:")
            print("Command sent to open WhatsApp.")
        except Exception as e:
            print(f"Failed to open WhatsApp: {e}")


def load_last_url():
    if os.path.exists(URL_HISTORY_FILE):
        with open(URL_HISTORY_FILE, 'r') as f:
            data = json.load(f)
            return data.get("last_url", "")
    return ""

def save_url(url):
    with open(URL_HISTORY_FILE, 'w') as f:
        json.dump({"last_url": url}, f)

def validate_url(url):
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url



# def smart_assistant():
#     phone = Mobile_Phone("Rudresh")
#     print("Welcome to Smart Assistant!")
#     while True:
#         user_input = input("\nCommand (or type 'exit'): ").strip().lower()
#         if user_input in ("exit", "quit", "close"):
#             break
#         elif match_command(user_input, ["camera", "photo"]):
#             threading.Thread(target=phone.ai_camera_capture_palm).start()
#         elif match_command(user_input, ["email"]):
#             threading.Thread(target=phone.launch_email_gui).start()
#         elif match_command(user_input, ["url", "browser"]):
#             threading.Thread(target=phone.launch_url_opener).start()
#         elif match_command(user_input, ["gallery"]):
#             threading.Thread(target=phone.open_gallery).start()
#         elif match_command(user_input, ["pdf"]):
#             threading.Thread(target=phone.open_pdf_viewer).start()
#         elif user_input in ("voice", "speak", "say", "mic", "voice command"):
#             command = listen_for_keyword()

#             if not command:
#                 speak("No command detected.")
#                 continue

#             if match_command(command, ["camera", "photo"]):
#                 speak("Launching AI Palm Camera.")
#                 threading.Thread(target=phone.ai_camera_capture_palm).start()

#             elif match_command(command, ["manual", "capture"]):
#                 speak("Taking manual photo.")
#                 threading.Thread(target=phone.manual_capture).start()

#             elif match_command(command, ["gallery", "image", "photo"]):
#                 speak("Opening image gallery.")
#                 threading.Thread(target=phone.open_gallery).start()

#             elif match_command(command, ["pdf", "document"]):
#                 speak("Opening PDF viewer.")
#                 threading.Thread(target=phone.open_pdf_viewer).start()

#             elif match_command(command, ["email", "gmail", "send mail"]):
#                 speak("Opening email sender.")
#                 threading.Thread(target=phone.launch_email_gui).start()

#             elif match_command(command, ["url", "browser", "web", "website"]):
#                 speak("Launching web opener.")
#                 threading.Thread(target=phone.launch_url_opener).start()

#             elif match_command(command, ["media", "music", "video", "play"]):
#                 speak("Please say the name of the media file to play.")
#                 query = listen_for_keyword()
#                 if query:
#                     result, msg = phone.play_media(query)
#                     speak(msg)
#                 else:
#                     speak("No media name recognized.")

#             elif match_command(command, ["scan", "load", "media files"]):
#                 speak("Scanning media files.")
#                 phone.scan_media_files()

#             elif match_command(command, ["contact", "contacts", "show contacts"]):
#                 speak("Fetching your saved contacts.")
#                 contacts = phone.get_contacts()
#                 if contacts:
#                     for name, number in contacts:
#                         speak(f"{name}: {number}")
#                 else:
#                     speak("No contacts found.")

#             elif match_command(command, ["call", "dial", "phone call"]):
#                 speak("Whom do you want to call?")
#                 name_or_number = listen_for_keyword()
#                 if name_or_number:
#                     result, msg = phone.make_call(name_or_number)
#                     speak(msg)
#                 else:
#                     speak("No contact name or number detected.")

#             else:
#                 speak("Sorry, I didn't recognize that voice command.")

#         else:
#             print("Unknown command. Try: camera, email, browser, gallery, pdf")


def run_gui():
    phone = Mobile_Phone("Rudresh")
    phone.start_alarm_checker()
    root = tk.Tk()
    root.title("📱 Rudresh's Virtual Phone")
    root.geometry("400x700")
    root.configure(bg="#dbeafe")

    # Group 1: Camera
    tk.Label(root, text="Camera", font=("Helvetica", 14, "bold"), bg="#dbeafe").pack(pady=5)
    tk.Button(root, text="📷 AI Palm Camera", command=phone.ai_camera_capture_palm, width=30).pack(pady=3)
    tk.Button(root, text="📸 Manual Photo", command=phone.manual_capture, width=30).pack(pady=3)

    # Group 2: Media & Gallery
    tk.Label(root, text="Media & Files", font=("Helvetica", 14, "bold"), bg="#dbeafe").pack(pady=10)
    tk.Button(root, text="🖼️ Open Gallery", command=phone.open_gallery, width=30).pack(pady=3)
    tk.Button(root, text="📄 Open PDF", command=phone.open_pdf_viewer, width=30).pack(pady=3)
    tk.Button(root, text="🎵 Scan Media", command=phone.scan_media_files, width=30).pack(pady=3)
    tk.Button(root, text="🎵 Scan Media", command=phone.scan_media_files, width=30).pack(pady=3)
    tk.Button(root, text="🎧 Play Media", command=phone.play_media_gui, width=30).pack(pady=3)

    # Group 3: Phone & Contacts
    tk.Label(root, text="Phone & Contacts", font=("Helvetica", 14, "bold"), bg="#dbeafe").pack(pady=10)
    tk.Button(root, text="📞 Make Call", command=lambda: phone.make_call_gui(), width=30).pack(pady=3)
    tk.Button(root, text="📇 View Contacts", command=phone.view_contacts_gui, width=30).pack(pady=3)
    tk.Button(root, text="➕ Save Contact", command=phone.save_contact_gui, width=30).pack(pady=3)

    # Group 4: Communication
    tk.Label(root, text="Communication", font=("Helvetica", 14, "bold"), bg="#dbeafe").pack(pady=10)
    tk.Button(root, text="✉️ Launch Email App", command=phone.launch_email_gui, width=30).pack(pady=3)
    tk.Button(root, text="🌐 Open Web App", command=phone.launch_url_opener, width=30).pack(pady=3)

    
    # Group 5: Utility Apps
    tk.Label(root, text="Utilities", font=("Helvetica", 14, "bold"), bg="#dbeafe").pack(pady=10)
    tk.Button(root, text="⏰ Alarm & Reminders", command=phone.launch_alarm_gui, width=30).pack(pady=3)
    tk.Button(root, text="WhatsApp", command=phone.open_whatsapp, width=30).pack(pady=3)
    tk.Button(root, text="YouTube", command=phone.open_youtube_brave, width=30).pack(pady=3)


    # Exit
    tk.Button(root, text="🚪 Exit App", command=root.destroy, bg="red", fg="white", width=30).pack(pady=20)

    root.mainloop()


if __name__ == '__main__':
    threading.Thread(target=run_gui).start()
    # smart_assistant()