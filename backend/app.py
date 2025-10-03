from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from whisper_utils import transcribe_audio
from flask_cors import CORS
from gpt_utils import analyze_lecture, chat_with_transcript

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global vars for chatbot
current_transcript = None
conversation_history = []


@app.route('/upload', methods=['POST'])
def upload_audio():
    global current_transcript, conversation_history

    try:
        # Check for uploaded file
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({'error': 'No audio file provided'}), 400

        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Transcribe audio and analyze
        transcript = transcribe_audio(filepath)
        result = analyze_lecture(transcript)

        # Reset conversation for new transcript
        current_transcript = transcript
        conversation_history = []

        return jsonify({
            'transcript': transcript,
            'analysis': result
        })

    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500


@app.route('/ask', methods=['POST'])
def ask_question():
    global current_transcript, conversation_history
    if not current_transcript:
        return jsonify({'error': 'No transcript available. Please upload audio first.'}), 400

    data = request.get_json()
    question = data.get('question', '').strip()

    if not question:
        return jsonify({'error': 'Question is required'}), 400

    try:
        # Add user message
        conversation_history.append({"role": "user", "content": question})

        # Generate answer with transcript + history
        answer = chat_with_transcript(current_transcript, conversation_history)

        # Save assistant reply
        conversation_history.append({"role": "assistant", "content": answer})

        return jsonify({
            'question': question,
            'answer': answer,
            'history': conversation_history
        })

    except Exception as e:
        return jsonify({'error': f'Error processing question: {str(e)}'}), 500


if __name__ == '__main__':
    import os
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

