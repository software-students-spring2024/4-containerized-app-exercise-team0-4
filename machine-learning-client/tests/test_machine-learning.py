# pylint: disable=missing-final-newline,missing-module-docstring,import-error
import pytest
from unittest.mock import patch, MagicMock, mock_open
from pymongo.results import InsertOneResult
from main import app, convert_mpeg_to_wav, transcribe_audio, save_transcription

class Tests:
    @pytest.fixture()
    def app(self):
        app.config.update({
            "TESTING": True,
        })

        # other setup can go here

        yield app

        # clean up / reset resources here

    @pytest.fixture()
    def client(self, app):
        return app.test_client()
    
    @staticmethod
    def test_sanity_check():
        expected = True
        actual = True
        assert actual == expected

    def test_convert_mpeg_to_wav_success(self):
        with patch('builtins.open', mock_open()) as mocked_file, \
            patch('os.remove') as mocked_os_remove, \
            patch('ffmpeg.input') as mocked_ffmpeg_input:
            mocked_output = mocked_ffmpeg_input.return_value.output.return_value
            mocked_output.run.return_value = None  # simulate successful run
            result = convert_mpeg_to_wav(b'sample binary data')
            assert result == 'output.wav'
            mocked_file.assert_called_once()
            mocked_os_remove.assert_called_once_with('temp_input.mpeg')

    def test_convert_mpeg_to_wav_failure(self):
        with patch('builtins.open', mock_open()) as mocked_file, \
            patch('os.remove') as mocked_os_remove, \
            patch('ffmpeg.input') as mocked_ffmpeg_input:
            mocked_output = mocked_ffmpeg_input.return_value.output.return_value
            mocked_output.run.side_effect = Exception("ffmpeg failure")
            result = convert_mpeg_to_wav(b'sample binary data')
            assert result is None
            mocked_file.assert_called_once()
            mocked_os_remove.assert_called_once_with('temp_input.mpeg')


    def test_transcribe_audio_success(self):
        with patch('speech_recognition.AudioFile') as mocked_audio_file, \
            patch('speech_recognition.Recognizer') as mocked_recognizer:
            mocked_recognizer_instance = mocked_recognizer.return_value
            mocked_recognizer_instance.recognize_sphinx.return_value = "Hello world"
            result = transcribe_audio('fakepath.wav')
            assert result == "Hello world"

    def test_transcribe_audio_failure(self):
        with patch('speech_recognition.AudioFile') as mocked_audio_file, \
            patch('speech_recognition.Recognizer') as mocked_recognizer:
            mocked_recognizer_instance = mocked_recognizer.return_value
            mocked_recognizer_instance.recognize_sphinx.side_effect = Exception("Recognition failed")
            result = transcribe_audio('fakepath.wav')
            assert result is None

    def test_upload_audio(client):
        with patch('main.convert_mpeg_to_wav') as mocked_convert, \
             patch('main.transcribe_audio') as mocked_transcribe, \
             patch('main.save_transcription') as mocked_save,  \
             patch('os.remove') as mocked_remove:
            mocked_convert.return_value = 'path_to_wav.wav'
            mocked_transcribe.return_value = 'Sample transcription'
            mocked_insert_one_result = MagicMock(spec=InsertOneResult)
            mocked_insert_one_result.inserted_id = "12345"
            mocked_save.return_value = mocked_insert_one_result
            response = app.test_client().post('/upload-audio', data=b'audio data here')
            assert response.status_code == 200
            assert b"Transcription saved successfully" in response.data
