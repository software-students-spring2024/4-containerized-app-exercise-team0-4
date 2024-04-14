import pytest
from app import app

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

    # Test to ensure the home route renders correctly
    def test_index_route(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'<a href="/record"><button>Start Recording</button></a>' in response.data

    # Test to ensure the view_transcription route renders correctly
    def test_record_route(self, client):
        response = client.get('/view_transcription')
        assert response.status_code == 200

    # Test to ensure the home route renders correctly
    def test_index_route(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'<a href="/record"><button>Start Recording</button></a>' in response.data
