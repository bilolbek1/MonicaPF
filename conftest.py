from monicapf.app import Monica
import pytest

@pytest.fixture
def app():
    return Monica()


@pytest.fixture
def test_client(app):
    return app.test_session()


