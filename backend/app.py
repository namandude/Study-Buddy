from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from whisper_utils import transcribe_audio
from flask_cors import CORS
from gpt_utils import analyze_lecture
import yt_dlp
import random

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def download_youtube_audio(youtube_url):
    """Download audio from YouTube video with anti-bot bypass"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(UPLOAD_FOLDER, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # Anti-bot bypass settings
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Connection': 'keep-alive',
        },
        'socket_timeout': 30,
        'retries': 10,
        'fragment_retries': 10,
        'ignoreerrors': False,
        'no_warnings': False,
        'extract_flat': False,
        'verbose': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info first
            info = ydl.extract_info(youtube_url, download=False)
            video_id = info.get('id', 'unknown')
            
            # Then download
            ydl.download([youtube_url])
            
            # Construct the expected file path
            audio_path = os.path.join(UPLOAD_FOLDER, f"{video_id}.mp3")
            
            # Wait a bit and check if file exists
            import time
            time.sleep(2)
            
            if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
                return audio_path
            else:
                # Try alternative path pattern
                alt_path = os.path.join(UPLOAD_FOLDER, f"{video_id}.webm.mp3")
                if os.path.exists(alt_path) and os.path.getsize(alt_path) > 0:
                    return alt_path
                else:
                    raise Exception("Downloaded file not found or empty")
                    
    except Exception as e:
        raise Exception(f"Error downloading YouTube video: {str(e)}")

def is_youtube_url(url):
    """Check if the provided string is a valid YouTube URL"""
    youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
    return any(domain in url for domain in youtube_domains)

@app.route('/upload', methods=['POST'])
def upload_audio():
    filepath = None
    is_youtube = False
    
    try:
        # Check if it's a file upload or YouTube URL
        if 'file' in request.files and request.files['file'].filename != '':
            # Handle file upload
            file = request.files['file']
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
        elif 'youtube_url' in request.form and request.form['youtube_url'].strip():
            # Handle YouTube URL
            youtube_url = request.form['youtube_url'].strip()
            
            # Validate YouTube URL
            if not is_youtube_url(youtube_url):
                return jsonify({'error': 'Please provide a valid YouTube URL'}), 400
                
            try:
                filepath = download_youtube_audio(youtube_url)
                is_youtube = True
            except Exception as e:
                return jsonify({'error': str(e)}), 400
        else:
            return jsonify({'error': 'No file or YouTube URL provided'}), 400

        # Process the audio file
        transcript = transcribe_audio(filepath)
        result = analyze_lecture(transcript)

        return jsonify({
            'transcript': transcript,
            'analysis': result
        })
        
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500
        
    finally:
        # Clean up the file if it was a YouTube download
        if is_youtube and filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass

if __name__ == '__main__':
    import os
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

# from flask import Flask, request, jsonify
# from werkzeug.utils import secure_filename
# import os
# from whisper_utils import transcribe_audio
# from flask_cors import CORS
# from gpt_utils import analyze_lecture

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/upload', methods=['POST'])
# def upload_audio():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file provided'}), 400
    
#     file = request.files['file']
    
#     if file.filename == '':
#         return jsonify({'error': 'Empty filename'}), 400

#     filename = secure_filename(file.filename)
#     filepath = os.path.join(UPLOAD_FOLDER, filename)
#     file.save(filepath)

#     transcript = transcribe_audio(filepath)
#     result = analyze_lecture(transcript)

#     return jsonify({
#         'transcript': transcript,
#         'analysis': result
#     })

# if __name__ == '__main__':
#     app.run(debug=True)
