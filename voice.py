import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import subprocess
import os
from pytube import YouTube
import whisper

class TranscriberApp:
    def __init__(self, root):
        self.root = root
        root.title("YouTube Audio Transcriber")
        
        tk.Label(root, text="YouTube URL:").pack()
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()

        tk.Label(root, text="Save Path:").pack()
        self.path_entry = tk.Entry(root, width=50)
        self.path_entry.pack()

        select_path_button = tk.Button(root, text="Select Save Path", command=self.select_save_path)
        select_path_button.pack()

        start_button = tk.Button(root, text="Start Transcribing", command=self.start_transcribing)
        start_button.pack()

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_transcribing, state=tk.DISABLED)
        self.stop_button.pack()

        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(root, length=200, variable=self.progress_var, maximum=100)
        progress_bar.pack()

        self.status_label = tk.Label(root, text="Idle")
        self.status_label.pack()

        self.stop_requested = False

    def select_save_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def start_transcribing(self):
        url = self.url_entry.get()
        save_path = self.path_entry.get()
        if not url or not save_path:
            messagebox.showerror("Error", "Please enter YouTube URL and select save path.")
            return
        self.stop_requested = False
        self.stop_button["state"] = tk.NORMAL
        threading.Thread(target=lambda: self.transcribe(url, save_path)).start()

    def stop_transcribing(self):
        self.stop_requested = True
        self.update_status("Stopping...")

    def transcribe(self, url, save_path):
        self.update_progress(0, "Downloading video...")
        if self.stop_requested:
            self.cleanup_and_stop()
            return
        video_file = self.download_youtube_video(url, save_path)
        audio_file = video_file.replace(".mp4", ".mp3")
        self.update_progress(25, "Extracting audio...")
        if self.stop_requested:
            self.cleanup_and_stop()
            return
        self.extract_audio_with_ffmpeg(video_file, audio_file)
        self.update_progress(50, "Transcribing audio...")
        if self.stop_requested:
            self.cleanup_and_stop()
            return
        text = self.transcribe_audio(audio_file)
        text_file_path = audio_file.replace(".mp3", ".txt")
        with open(text_file_path, "w", encoding="utf-8") as text_file:
            text_file.write(text)
        self.update_progress(100, "Transcription completed!")
        messagebox.showinfo("Transcription Completed", f"The audio has been successfully transcribed.\nSaved to {text_file_path}")
        self.stop_button["state"] = tk.DISABLED

    def download_youtube_video(self, url, path):
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=path, filename=f"{yt.title}.mp4")
        return os.path.join(path, f"{yt.title}.mp4")

    def extract_audio_with_ffmpeg(self, input_video_path, output_audio_path):
        command = [
            'ffmpeg',
            '-i', input_video_path,
            '-vn',
            '-ab', '128k',
            '-ar', '44100',
            '-y',
            output_audio_path
        ]
        subprocess.run(command, check=True)

    def transcribe_audio(self, audio_file):
        model = whisper.load_model("large")
        result = model.transcribe(audio_file)
        return result["text"]

    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def update_progress(self, progress, message):
        self.progress_var.set(progress)
        self.update_status(message)

    def cleanup_and_stop(self):
        self.update_progress(0, "Operation stopped.")
        self.stop_button["state"] = tk.DISABLED

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriberApp(root)
    root.mainloop()
