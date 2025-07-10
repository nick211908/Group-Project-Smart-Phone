# pdf_viewer.py
import sys
import os
import webview

def run_pdf_viewer(pdf_path):
    file_url = "file:///" + os.path.abspath(pdf_path).replace("\\", "/")
    window = webview.create_window("📄 PDF Viewer", file_url, width=900, height=700, resizable=True)
    webview.start(gui='tkinter')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("❌ No PDF path provided.")
    else:
        run_pdf_viewer(sys.argv[1])
