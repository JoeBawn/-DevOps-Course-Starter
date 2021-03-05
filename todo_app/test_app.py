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
    board_id = os.getenv('TRELLO_API_BOARD_ID')
    if url.startswith(f'https://api.trello.com/1/boards/{trello_board_id}/lists'):
        response = Mock()

        sample_trello_lists_response = [
            {
                "id": "601841a7adc438808cfe44b5",
                "name": "To Do",
                "closed": false,
                "pos": 4096,
                "softLimit": null,
                "idBoard": "5ff48f05dd6ab805185a793b",
                "subscribed": false
            },
            {
                "id": "5ff48f05dd6ab805185a793d",
                "name": "In Progress",
                "closed": false,
                "pos": 32768,
                "softLimit": null,
                "idBoard": "5ff48f05dd6ab805185a793b",
                "subscribed": false
            },
            {
                "id": "5ff48f05dd6ab805185a793e",
                "name": "Completed",
                "closed": false,
                "pos": 49152,
                "softLimit": null,
                "idBoard": "5ff48f05dd6ab805185a793b",
                "subscribed": false
            }
        ]
        response.json.return_value = sample_trello_lists_response
        return response
    elif url.startswith(f'https://api.trello.com/1/boards/{trello_board_id}/cards'):
        response = Mock()

        sample_trello_lists_response = [
                {
                    "id": "603faf7a380d8722d64ec579",
                    "checkItemStates": null,
                    "closed": false,
                    "dateLastActivity": "2021-03-03T15:47:06.248Z",
                    "desc": "New Test",
                    "descData": null,
                    "dueReminder": null,
                    "idBoard": "5ff48f05dd6ab805185a793b",
                    "idList": "601841a7adc438808cfe44b5",
                    "idMembersVoted": [],
                    "idShort": 28,
                    "idAttachmentCover": null,
                    "idLabels": [],
                    "manualCoverAttachment": false,
                    "name": "New Test",
                    "pos": 98304,
                    "shortLink": "NyMaqAAC",
                    "isTemplate": false,
                    "cardRole": null,
                    "badges": {
                        "attachmentsByType": {
                            "trello": {
                                "board": 0,
                                "card": 0
                            }
                        },
                        "location": false,
                        "votes": 0,
                        "viewingMemberVoted": false,
                        "subscribed": false,
                        "fogbugz": "",
                        "checkItems": 0,
                        "checkItemsChecked": 0,
                        "checkItemsEarliestDue": null,
                        "comments": 0,
                        "attachments": 0,
                        "description": true,
                        "due": "2021-04-02T00:00:00.000Z",
                        "dueComplete": false,
                        "start": null
                    },
                    "dueComplete": false,
                    "due": "2021-04-02T00:00:00.000Z",
                    "idChecklists": [],
                    "idMembers": [],
                    "labels": [],
                    "shortUrl": "https://trello.com/c/NyMaqAAC",
                    "start": null,
                    "subscribed": false,
                    "url": "https://trello.com/c/NyMaqAAC/28-new-test",
                    "cover": {
                        "idAttachment": null,
                        "color": null,
                        "idUploadedBackground": null,
                        "size": "normal",
                        "brightness": "light",
                        "idPlugin": null
                    }
                },
                {
                    "id": "6042162ef8aeae6ffa565dc8",
                    "checkItemStates": null,
                    "closed": false,
                    "dateLastActivity": "2021-03-05T11:29:50.819Z",
                    "desc": "asfsd",
                    "descData": null,
                    "dueReminder": null,
                    "idBoard": "5ff48f05dd6ab805185a793b",
                    "idList": "601841a7adc438808cfe44b5",
                    "idMembersVoted": [],
                    "idShort": 35,
                    "idAttachmentCover": null,
                    "idLabels": [],
                    "manualCoverAttachment": false,
                    "name": "sdhjfaj",
                    "pos": 114688,
                    "shortLink": "sMVXFy8t",
                    "isTemplate": false,
                    "cardRole": null,
                    "badges": {
                        "attachmentsByType": {
                            "trello": {
                                "board": 0,
                                "card": 0
                            }
                        },
                        "location": false,
                        "votes": 0,
                        "viewingMemberVoted": false,
                        "subscribed": false,
                        "fogbugz": "",
                        "checkItems": 0,
                        "checkItemsChecked": 0,
                        "checkItemsEarliestDue": null,
                        "comments": 0,
                        "attachments": 0,
                        "description": true,
                        "due": "2021-04-04T00:00:00.000Z",
                        "dueComplete": false,
                        "start": null
                    },
                    "dueComplete": false,
                    "due": "2021-04-04T00:00:00.000Z",
                    "idChecklists": [],
                    "idMembers": [],
                    "labels": [],
                    "shortUrl": "https://trello.com/c/sMVXFy8t",
                    "start": null,
                    "subscribed": false,
                    "url": "https://trello.com/c/sMVXFy8t/35-sdhjfaj",
                    "cover": {
                        "idAttachment": null,
                        "color": null,
                        "idUploadedBackground": null,
                        "size": "normal",
                        "brightness": "light",
                        "idPlugin": null
                    }
                }
        ]
        response.json.return_value = sample_trello_lists_response
        return response
    return None


