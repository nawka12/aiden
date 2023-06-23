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
## FAQ
Q: Why it's so slow?

A: There are several factors. The first one is your internet connection. The second one is your PC specification, since Aiden utilize CPU, GPU, and RAM.
## Known bugs
- The stop button will not stop the transcription immediately. It will processes the last chunk downloaded until it's transcribed, and then completely stop.
- If you want to utilize your GPU, please install the GPU version of torch (in the venv for batch file user).
