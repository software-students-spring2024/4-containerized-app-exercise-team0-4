from flask import Flask, request, jsonify
from pymongo import MongoClient
import speech_recognition as sr

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['audio-transcriptions']
collection = db['transcriptions']

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    # Receive audio file from frontend
    audio_file = request.files['audio']

    # Transcribe the audio file (this is a placeholder function)
    transcription = transcribe_audio(audio_file)

    print("Transcription:", transcription)

    # Save transcription to MongoDB
    if transcription:
        transcription_data = {
            'transcription': transcription,
            # Add any additional metadata
        }
        result = collection.insert_one(transcription_data)
        return jsonify({'message': 'Transcription saved successfully', 'id': str(result.inserted_id)})
    else:
        return jsonify({'error': 'Transcription failed'})

def transcribe_audio(audio_file):
    # Placeholder function for transcribing audio
    # You would replace this with your actual transcription logic
    # For example, using a speech-to-text service or library
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
        try:
            return r.recognize_sphinx(audio_data, language='en-US')
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None

if __name__ == '__main__':
    app.run(debug=True)
