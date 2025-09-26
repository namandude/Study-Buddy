import shutil
import whisper

# Check if ffmpeg is available
if shutil.which("ffmpeg") is None:
    raise EnvironmentError(
        "ffmpeg is not installed. On Render, install it in the build command."
    )

# Load Whisper model
model = whisper.load_model("base")

def transcribe_audio(file_path):
    """
    Transcribe audio file to text using Whisper model.
    Returns:
        str: transcript text
    """
    result = model.transcribe(file_path, fp16=False)
    return result["text"]


# import os

# # Add ffmpeg bin folder to PATH
# os.environ["PATH"] += os.pathsep + r"F:\ffmpeg-8.0-essentials_build\ffmpeg-8.0-essentials_build\bin"

# import whisper

# model = whisper.load_model("base")
# def transcribe_audio(file_path):
#   result = model.transcribe(file_path, fp16=False) 
#   return result["text"]

  