# tools_app_launcher.py

import subprocess
import webbrowser
import os
import shutil
from livekit.agents import function_tool, RunContext

@function_tool()
async def open_youtube(context: RunContext, query: str = "") -> str:
    url = "https://www.youtube.com"
    if query:
        query = query.strip().replace(" ", "+")
        url = f"{url}/results?search_query={query}"

    brave_path = shutil.which("brave") or r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    if os.path.exists(brave_path):
        subprocess.Popen([brave_path, url])
        return f"Opened YouTube{' search for ' + query if query else ''} in Brave browser."
    else:
        webbrowser.open(url)
        return f"Opened YouTube{' search for ' + query if query else ''} in default browser."

@function_tool()
async def open_gmail(context: RunContext) -> str:
    chrome_path = shutil.which("chrome") or r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    url = "https://mail.google.com"

    if os.path.exists(chrome_path):
        subprocess.Popen([chrome_path, url])
        return "Opened Gmail in Chrome browser."
    else:
        webbrowser.open(url)
        return "Opened Gmail in default browser."

@function_tool()
async def open_whatsapp(context: RunContext) -> str:
    try:
        subprocess.Popen(["explorer.exe", "shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"])
        return "Opened WhatsApp."
    except Exception as e:
        return f"Failed to open WhatsApp: {e}"
