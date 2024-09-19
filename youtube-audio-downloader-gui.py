import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os

def download_audio(url, output_dir):
    try:
        command = [
            'yt-dlp',
            '-f', 'bestaudio',
            '--extract-audio',
            '--audio-format', 'mp3',
            '-o', f'{output_dir}/%(title)s.%(ext)s',
            url
        ]
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def start_download():
    urls = url_entry.get("1.0", tk.END).strip().split("\n")
    output_dir = output_dir_entry.get()

    if not urls or urls[0] == "":
        messagebox.showerror("Error", "Please enter at least one URL.")
        return

    if not output_dir:
        messagebox.showerror("Error", "Please select an output directory.")
        return

    progress_text.delete("1.0", tk.END)
    download_button.config(state=tk.DISABLED)

    def download_thread():
        for url in urls:
            progress_text.insert(tk.END, f"Starting download for: {url}\n")
            success = download_audio(url, output_dir)
            if success:
                progress_text.insert(tk.END, f"Download completed for: {url}\n")
            else:
                progress_text.insert(tk.END, f"Error downloading: {url}\n")
            progress_text.see(tk.END)

        progress_text.insert(tk.END, "All downloads completed.\n")
        download_button.config(state=tk.NORMAL)

    threading.Thread(target=download_thread, daemon=True).start()

def select_output_dir():
    folder = filedialog.askdirectory()
    if folder:
        output_dir_entry.delete(0, tk.END)
        output_dir_entry.insert(0, folder)

# Create main window
root = tk.Tk()
root.title("YouTube Audio Downloader")
root.geometry("600x400")

# URL input
url_label = tk.Label(root, text="Enter YouTube URLs (one per line):")
url_label.pack(pady=(10, 0))
url_entry = tk.Text(root, height=5)
url_entry.pack(padx=10, pady=(0, 10), fill=tk.X)

# Output directory selection
output_dir_frame = tk.Frame(root)
output_dir_frame.pack(fill=tk.X, padx=10)

output_dir_label = tk.Label(output_dir_frame, text="Output Directory:")
output_dir_label.pack(side=tk.LEFT)

output_dir_entry = tk.Entry(output_dir_frame)
output_dir_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

output_dir_button = tk.Button(output_dir_frame, text="Browse", command=select_output_dir)
output_dir_button.pack(side=tk.LEFT)

# Download button
download_button = tk.Button(root, text="Download", command=start_download)
download_button.pack(pady=10)

# Progress display
progress_label = tk.Label(root, text="Download Progress:")
progress_label.pack()
progress_text = tk.Text(root, height=10, wrap=tk.WORD)
progress_text.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

root.mainloop()
