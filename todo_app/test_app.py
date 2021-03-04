import os, pytest, json, datetime
import todo_app.app
from dotenv import find_dotenv, load_dotenv
from unittest.mock import patch, Mock

trello_board_id = os.getenv('TRELLO_API_BOARD_ID')

@pytest.fixture
def client():
    # Use our test integration config instead of the
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    
    # Create the new app.
    test_app = todo_app.app.create_app()
    
    # Use the app to create a test_client that can be
    with test_app.test_client() as client:
        yield client

@patch('requests.get')
def test_index_page(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    
    mock_get_request.side_effect = mock_trello_lists
    response = client.get('/')

    assert b'Apple' in response.data
    assert b'Bannana' in response.data
    assert b'Orange' in response.data
    assert b'Pear' in response.data

def mock_trello_lists(url):
    board_id = os.getenv('TRELLO_API_BOARD_ID')
    if url.startswith(f'https://api.trello.com/1/boards/{trello_board_id}/lists'):
        response = Mock()
        # sample_trello_lists_response should point to some test response data
        response.json.return_value = sample_trello_lists_response
        return response
        
    return None


