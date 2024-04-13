from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import speech_recognition as sr
import ffmpeg


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
client = MongoClient("mongodb://localhost:27017/")
db = client["audio-transcriptions"]
collection = db["transcriptions"]

@app.route("/upload-audio", methods=["POST"])
@cross_origin()  # Allow cross-origin access for this route
def upload_audio():
    
    def convert_mpeg_to_wav(binary_data):

        with open('temp_input.mpeg', 'wb') as temp_file:
            temp_file.write(binary_data)

        try:
            # Convert the MPEG file to WAV using ffmpeg
            (
                ffmpeg
                .input('temp_input.mpeg')
                .output('output.wav', format='wav')
                .run(overwrite_output=True)
            )
            print("Conversion successful!")
        except ffmpeg.Error as e:
            print("An error occurred:", e)

        # Clean up temporary file
        import os
        os.remove('temp_input.mpeg')

    # Receive audio file from frontend
    audio_data = request.data
    # convert to .wav
    convert_mpeg_to_wav(audio_data)
    transcription = transcribe_audio("output.wav")
    
    print("Transcription:", transcription)
    

    '''
    # Save transcription to MongoDB
    if transcription:
        transcription_data = {
            "transcription": transcription,
            # username won't be passed through form, but post body
            "username": request.form.get("username"),
            "date_created": request.form.get("date_created"),
        }
        result = collection.insert_one(transcription_data)
        return jsonify(
            {
                "message": "Transcription saved successfully",
                "id": str(result.inserted_id),
            }
        )
    else:
        return jsonify({"error": "Transcription failed"})
    '''
    return jsonify({
        "message": "Audio received",
        "transcript": transcription
        })


def transcribe_audio(audio_file):

    # Placeholder function for transcribing audio
    # You would replace this with your actual transcription logic
    # For example, using a speech-to-text service or library
    r = sr.Recognizer()
    print(audio_file)  
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
        print(type(audio_data))
        
        transcription = r.recognize_sphinx(audio_data)
        print(transcription)
        return transcription
        '''
        try:
            return r.recognize_sphinx(audio, language="en-US")
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None
        '''
            


if __name__ == "__main__":
    app.run(debug=True, port=3001)
