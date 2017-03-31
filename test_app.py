import pytest
import route_grabber

@pytest.fixture
def app():
    return route_grabber.app


@pytest.fixture
def test_client(app):
    return app.test_client()


def test_hello(test_client):
    """
    GIVEN: A flask hello app
    WHEN: I GET the hello/ route
    THEN: The response should be "Hello World!"
    """
    response = test_client.get("/hello")
    assert response.data.decode("utf-8") == "Hello World!"
