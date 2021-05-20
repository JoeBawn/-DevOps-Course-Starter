import os, pytest, json, datetime
import todo_app.app
import dotenv
from unittest.mock import patch, Mock

trello_board_id = os.getenv('TRELLO_API_BOARD_ID')

@pytest.fixture
def client():
    file_path = dotenv.find_dotenv('.env.test') 
    dotenv.load_dotenv(file_path, override=True)
    
    test_app = todo_app.app.create_app()
    
    with test_app.test_client() as client:
        yield client

@patch('requests.get')
def test_index_page(mock_get_requests, client):
    
    mock_get_requests.side_effect = mock_trello_request
    response = client.get('/')

    assert b'New Test' in response.data
    assert b'sdhjfaj' in response.data

def mock_trello_request(url):
    trello_board_id = os.getenv('TRELLO_API_BOARD_ID')
    if url.startswith(f'https://api.trello.com/1/boards/{trello_board_id}/lists'):
        response = Mock()

        sample_trello_lists_response = [
            {
                "id": "601841a7adc438808cfe44b5",
                "name": "To Do",
                "closed": False,
                "pos": 4096,
                "softLimit": None,
                "idBoard": "5ff48f05dd6ab805185a793b",
                "subscribed": False
            },
            {
                "id": "5ff48f05dd6ab805185a793d",
                "name": "Doing",
                "closed": False,
                "pos": 32768,
                "softLimit": None,
                "idBoard": "5ff48f05dd6ab805185a793b",
                "subscribed": False
            },
            {
                "id": "5ff48f05dd6ab805185a793e",
                "name": "Done",
                "closed": False,
                "pos": 49152,
                "softLimit": None,
                "idBoard": "5ff48f05dd6ab805185a793b",
                "subscribed": False
            }
        ]
        response.json.return_value = sample_trello_lists_response
        return response
    elif url.startswith(f'https://api.trello.com/1/boards/{trello_board_id}/cards'):
        response = Mock()

        sample_trello_lists_response = [
                {
                    "id": "603faf7a380d8722d64ec579",
                    "checkItemStates": None,
                    "closed": False,
                    "dateLastActivity": "2021-03-03T15:47:06.248Z",
                    "desc": "New Test",
                    "descData": None,
                    "dueReminder": None,
                    "idBoard": "5ff48f05dd6ab805185a793b",
                    "idList": "601841a7adc438808cfe44b5",
                    "idMembersVoted": [],
                    "idShort": 28,
                    "idAttachmentCover": None,
                    "idLabels": [],
                    "manualCoverAttachment": False,
                    "name": "New Test",
                    "pos": 98304,
                    "shortLink": "NyMaqAAC",
                    "isTemplate": False,
                    "cardRole": None,
                    "badges": {
                        "attachmentsByType": {
                            "trello": {
                                "board": 0,
                                "card": 0
                            }
                        },
                        "location": False,
                        "votes": 0,
                        "viewingMemberVoted": False,
                        "subscribed": False,
                        "fogbugz": "",
                        "checkItems": 0,
                        "checkItemsChecked": 0,
                        "checkItemsEarliestDue": None,
                        "comments": 0,
                        "attachments": 0,
                        "description": True,
                        "due": "2021-04-02T00:00:00.000Z",
                        "dueComplete": False,
                        "start": None
                    },
                    "dueComplete": False,
                    "due": "2021-04-02T00:00:00.000Z",
                    "idChecklists": [],
                    "idMembers": [],
                    "labels": [],
                    "shortUrl": "https://trello.com/c/NyMaqAAC",
                    "start": None,
                    "subscribed": False,
                    "url": "https://trello.com/c/NyMaqAAC/28-new-test",
                    "cover": {
                        "idAttachment": None,
                        "color": None,
                        "idUploadedBackground": None,
                        "size": "normal",
                        "brightness": "light",
                        "idPlugin": None
                    }
                },
                {
                    "id": "6042162ef8aeae6ffa565dc8",
                    "checkItemStates": None,
                    "closed": False,
                    "dateLastActivity": "2021-03-05T11:29:50.819Z",
                    "desc": "asfsd",
                    "descData": None,
                    "dueReminder": None,
                    "idBoard": "5ff48f05dd6ab805185a793b",
                    "idList": "601841a7adc438808cfe44b5",
                    "idMembersVoted": [],
                    "idShort": 35,
                    "idAttachmentCover": None,
                    "idLabels": [],
                    "manualCoverAttachment": False,
                    "name": "sdhjfaj",
                    "pos": 114688,
                    "shortLink": "sMVXFy8t",
                    "isTemplate": False,
                    "cardRole": None,
                    "badges": {
                        "attachmentsByType": {
                            "trello": {
                                "board": 0,
                                "card": 0
                            }
                        },
                        "location": False,
                        "votes": 0,
                        "viewingMemberVoted": False,
                        "subscribed": False,
                        "fogbugz": "",
                        "checkItems": 0,
                        "checkItemsChecked": 0,
                        "checkItemsEarliestDue": None,
                        "comments": 0,
                        "attachments": 0,
                        "description": True,
                        "due": "2021-04-04T00:00:00.000Z",
                        "dueComplete": False,
                        "start": None
                    },
                    "dueComplete": False,
                    "due": "2021-04-04T00:00:00.000Z",
                    "idChecklists": [],
                    "idMembers": [],
                    "labels": [],
                    "shortUrl": "https://trello.com/c/sMVXFy8t",
                    "start": None,
                    "subscribed": False,
                    "url": "https://trello.com/c/sMVXFy8t/35-sdhjfaj",
                    "cover": {
                        "idAttachment": None,
                        "color": None,
                        "idUploadedBackground": None,
                        "size": "normal",
                        "brightness": "light",
                        "idPlugin": None
                    }
                }
        ]
        response.json.return_value = sample_trello_lists_response
        return response
    return None


