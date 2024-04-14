import pytest
from app import app

class Tests:
    """
    This class contains test cases for the web app.
    """
    @pytest.fixture()
    def app(self):
        """
        Fixture to set up the app for testing.

        Returns:
            Flask app: The Flask app object.
        """
        app.config.update({
            "TESTING": True,
        })
        yield app

    @pytest.fixture()
    def client(self, app):
        """
        Fixture to get the test client.

        Args:
            app (Flask app): The Flask app object.

        Returns:
            Flask test client: The Flask test client object.
        """
        return app.test_client()


    @staticmethod
    def test_sanity_check():
        """
        Test case to check the sanity of the testing framework.
        """
        expected = True
        actual = True
        assert actual == expected

    def test_index_route(self, client):
        """
        Test case to ensure the home route renders correctly.

        Args:
            client (Flask test client): The Flask test client object.
        """
        response = client.get('/')
        assert response.status_code == 200
        assert b'<a href="/record"><button>Start Recording</button></a>' in response.data

    def test_record_route(self, client):
        """
        Test case to ensure the record route renders correctly.

        Args:
            client (Flask test client): The Flask test client object.
        """
        response = client.get('/record')
        assert response.status_code == 200
        assert b'<h1 style="font-size: 24px;">Record Memo</h1>' in response.data