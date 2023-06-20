import tkinter as tk
import threading
import yt_dlp
import os
import whisper
from googletrans import Translator
import subprocess

# YouTube-DL options
ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'format-sort': 'acodec:aac',
    'cookies-from-browser': 'brave'
}

# Whisper model
model = whisper.load_model("small")

# Output directory for audio fragments
output_directory = "audio_fragments"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# GUI window
window = tk.Tk()
window.title("Aiden YT-Stream Transcriber")

# YouTube link label and entry
youtube_link_label = tk.Label(window, text="YouTube Link:")
youtube_link_label.pack()
youtube_link_entry = tk.Entry(window, width=50)
youtube_link_entry.pack()

# Destination language label and entry
dest_language_label = tk.Label(window, text="Destination Language:")
dest_language_label.pack()
dest_language_entry = tk.Entry(window, width=5)
dest_language_entry.pack()
dest_language_entry.insert(tk.END, "en")  # Fill with "en" by default

# Transcription text area
transcription_text = tk.Text(window, height=20, width=50)
transcription_text.pack()

# Thread for audio processing
audio_thread = None
stop_audio_processing = threading.Event()  # Event to stop the audio processing loop

def process_audio_chunk(start_time, end_time, livestream_url):
    global stop_audio_processing

    current_chunk = 0

    # Download the audio fragment using yt-dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(livestream_url, download=False)
            audio_url = info['url']
            output_filename = f"{output_directory}/livestream_chunk_maiden.mp3"
            command = f'ffmpeg -y -ss {start_time} -i "{audio_url}" -t {end_time - start_time} -vn -c:a libmp3lame -q:a 2 "{output_filename}"'

            # Use subprocess to capture console output
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            _, error_output = process.communicate()

            if process.returncode != 0:
                error_message = error_output.decode('utf-8')
                window.after(0, lambda: print(f"An error occurred: {error_message}"))

                # Check if the error contains "403 Forbidden" or "Failed to open segment"
                if "403 Forbidden" in error_message or "Failed to open segment" in error_message:
                    # Stop the audio processing if HTTP 403 Forbidden or Failed to open segment error occurs
                    stop_audio_processing.set()
                    window.after(0, lambda: print("Transcription stopped due to YT-dlp error."))
                return

            window.after(0, lambda: print(f"Audio fragment {start_time}-{end_time} downloaded and converted successfully!"))

            # Load the audio fragment
            audio_data = whisper.load_audio(output_filename)

            # Transcribe the audio chunk using Whisper
            transcription = model.transcribe(audio_data)

            # Translate with GTL
            dest_language = dest_language_entry.get()
            if not dest_language:
                dest_language = "en"  # Fill with "en" if empty

            translator = Translator()
            try:
                translations = translator.translate(f"{transcription['text']}", dest=dest_language)
                # Print to console
                window.after(0, lambda: print(f"AUTO: {transcription['text']}"))
                window.after(0, lambda: print(f"TL: {translations.text}"))

                # Update the GUI with the transcription
                window.after(0, lambda: transcription_text.insert(tk.END, f"Transcription ({start_time}-{end_time}): {transcription['text']}\n\n"))
                window.after(0, lambda: transcription_text.insert(tk.END, f"Translation ({start_time}-{end_time}): {translations.text}\n\n"))
                window.after(0, transcription_text.see, tk.END)
            except Exception as e:
                window.after(0, lambda err=e: print(f"An error occurred during translation: {str(err)}"))
        except yt_dlp.DownloadError as e:
            window.after(0, lambda err=e: print(f"An error occurred: {str(err)}"))
            if "403 Forbidden" in str(e) or "Failed to open segment" in str(e):
                # Stop the audio processing if HTTP 403 Forbidden or Failed to open segment error occurs
                stop_audio_processing.set()
                window.after(0, lambda: print("Transcription stopped due to YT-dlp error."))

    if current_chunk > 0:
        previous_chunk_filename = f"livestream_chunk_maiden_{current_chunk - 1}.mp3"
        os.remove(previous_chunk_filename)

def start_transcription():
    global audio_thread

    if audio_thread is None or not audio_thread.is_alive():
        # Start the transcription
        livestream_url = youtube_link_entry.get()
        if livestream_url:
            youtube_link_entry.config(state=tk.DISABLED)
            dest_language_entry.config(state=tk.DISABLED)
            start_button.config(state=tk.DISABLED)
            stop_button.config(state=tk.NORMAL)  # Enable the stop button
            audio_thread = threading.Thread(target=process_audio_chunks, args=(livestream_url,))
            stop_audio_processing.clear()  # Reset the stop flag
            audio_thread.start()

def stop_transcription():
    global stop_audio_processing

    if audio_thread is not None and audio_thread.is_alive():
        # Set the stop flag to stop the transcription loop
        stop_audio_processing.set()
        stop_button.config(state=tk.DISABLED)  # Disable the stop button temporarily
        transcription_text.delete('1.0', tk.END)  # Clear the transcription text

def process_audio_chunks(livestream_url):
    start_time = 0
    chunk_duration = 10  # Set the chunk duration to 10 seconds

    while not stop_audio_processing.is_set():
        end_time = start_time + chunk_duration

        process_audio_chunk(start_time, end_time, livestream_url)

        start_time = end_time

        # Check if the livestream has finished using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(livestream_url, download=False)
                duration = info.get('duration')
            except yt_dlp.DownloadError as e:
                print(f"An error occurred: {str(e)}")
                break

        if duration is not None and start_time >= duration:
            break

    # Reset the GUI state after the transcription is completed or stopped
    window.after(0, lambda: youtube_link_entry.config(state=tk.NORMAL))
    window.after(0, lambda: dest_language_entry.config(state=tk.NORMAL))
    window.after(0, lambda: start_button.config(state=tk.NORMAL))
    window.after(0, lambda: stop_button.config(state=tk.DISABLED))

# Start button
start_button = tk.Button(window, text="Start", width=20, command=start_transcription)
start_button.pack()

# Stop button
stop_button = tk.Button(window, text="Stop", width=20, command=stop_transcription)
stop_button.pack()

# Start the GUI event loop
window.mainloop()
