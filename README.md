# Aiden
Livestream Transcriber & Translator using OpenAI Whisper (non-API)

# WIP

## How to run Aiden?
Make sure you have Python installed on your system (tested with Python 3.10.6).
```
pip install -r requirements.txt
py main.py
```
For Windows users, you can simply use the run.bat file. The batch file will install all the dependencies. Please note that on the first run, run.bat will automatically close after the installation is finished. This is normal behavior. You can open it again to run Aiden.

## FAQ
Q: Why is it so slow?

A: There are several factors that can contribute to the speed. The first one is your internet connection. The second one is your PC specifications since Aiden utilizes CPU, GPU, and RAM.

## Known bugs
- The stop button will not immediately stop the transcription. It will continue processing the last downloaded chunk until it is transcribed and then completely stop.
- If you want to utilize your GPU, please install the GPU version of Torch (in the venv for batch file users). The default installation does not automatically install the GPU version of PyTorch.
