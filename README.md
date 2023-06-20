# Aiden
Livestream Transcriber &amp; Translator using OpenAI Whisper (non-API)

# WIP

## How to run Aiden?
Make sure you have Python installed on your system (tested with Python 3.10.6)
```
pip install -r requirements.txt
py main.py
```
Or for you Windows user, simply use `run.bat` file. The batch file will install all the dependencies. 
Please note that on the first run, `run.bat` will automatically close after the installation finished. This is normal, you can open it again to run Aiden.

## Known bugs
- The transcription will froze when `yt-dlp` starting to receive HTTP 403 Forbidden error. Please do `KeyboardInterrupt` (Ctrl + C) or close the batch window to stop Aiden, and run it again.
- If you want to utilize your GPU, please install the GPU version of torch in the venv.
- Window resize is not working properly yet.
