from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import speech_recognition as sr
import ffmpeg
import logging
import os
import datetime
app = Flask(__name__)
CORS(app, supports_credentials=True)

# DB Set up
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


@app.route("/upload-audio", methods=["POST", "OPTIONS"])
@cross_origin(origins="*", supports_credentials=True)
def upload_audio():
    print("call made")
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
    
# create a simple get just to test the server
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Server is up and running!"})

if __name__ == "__main__":
    app.run(debug=True)