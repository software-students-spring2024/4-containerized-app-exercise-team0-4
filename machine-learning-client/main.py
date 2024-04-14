from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import speech_recognition as sr
import ffmpeg
import logging
import os
import datetime
'''
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PW = os.getenv("DB_PW")


client = MongoClient(f"mongodb+srv://{DB_USER}:{DB_PW}@sweproject2.v6vtrh6.mongodb.net/sweproject4?retryWrites=true&w=majority&appName=SWEProject2")
'''
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
client = MongoClient("mongodb://localhost:27017/")
db = client["audio-transcriptions"]
collection = db["transcriptions"]

def convert_mpeg_to_wav(binary_data):
        temp_file_path = 'temp_input.mpeg'
        output_wav_path = 'output.wav'
        
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(binary_data)

        try:
            # Convert the MPEG file to WAV using ffmpeg
            ffmpeg.input(temp_file_path).output(output_wav_path, format='wav').run(overwrite_output=True)
            logging.info("Conversion successful!")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None  # Return None if conversion fails
        finally:
            os.remove(temp_file_path)

        return output_wav_path

def transcribe_audio(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
        try:
            transcription = r.recognize_sphinx(audio_data)
            return transcription
        except Exception as e:
            logging.error(f"Speech recognition error: {e}")
            return None
        
def save_transcription(transcription):
    transcription_data = {
            "transcription": transcription,
            "username": "DefaultUser",  # Using a default username
            "date_created": datetime.datetime.utcnow()  # Automatically setting the date to now
        }
    result = collection.insert_one(transcription_data)
    return result


@app.route("/upload-audio", methods=["POST"])
@cross_origin()  # Allow cross-origin access for this route
def upload_audio():
    # Receive audio file from frontend
    print(request.data)
    audio_data = request.data

    # Convert to .wav and get the path to the converted file
    wav_file_path = convert_mpeg_to_wav(audio_data)

    if not wav_file_path:
        return jsonify({"error": "Failed to convert audio file"}), 500

    transcription = transcribe_audio(wav_file_path)
    
    # Clean up WAV file after transcription
    os.remove(wav_file_path)
    
    logging.info(f"Transcription: {transcription}")

    # Check for transcription and save to MongoDB
    if transcription:
        result = save_transcription(transcription)
        return jsonify({
            "message": "Transcription saved successfully",
            "transcript": transcription,
            "id": str(result.inserted_id)
        })
    else:
        return jsonify({"error": "Transcription failed"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=3001)