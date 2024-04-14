import pytest
from unittest.mock import patch
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

    
    # Test to ensure the record route renders correctly
    def test_record_route(self, client):
        response = client.get('/record')
        assert response.status_code == 200
        assert b'<h1 style="font-size: 24px;">Record Memo</h1>' in response.data

