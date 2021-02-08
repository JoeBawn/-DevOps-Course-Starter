import os
import requests

class TrelloCard:
    def __init__(self, id, name, idList):
        self.id = id
        self.name = name
        self.idList = idList

def get_trello_credentials():
    auth_cred = []
    auth_cred.append(os.getenv('TRELLO_API_KEY'))
    auth_cred.append(os.getenv('TRELLO_API_TOKEN'))

    return auth_cred

def get_trello_board_id():
    board_id = os.getenv('TRELLO_API_BOARD_ID')
    return board_id

def get_trello_lists_on_board():
    trello_auth_cred = get_trello_credentials()
    trello_board_id = get_trello_board_id()
    getalllistsparams = {'key': trello_auth_cred[0], 'token': trello_auth_cred[1]}
    response = requests.get(f'https://api.trello.com/1/boards/{trello_board_id}/lists', params=getalllistsparams)
    all_lists = response.json()

    return all_lists


def get_trello_list_id(list_name):
    trello_auth_cred = get_trello_credentials()
    trello_board_id = get_trello_board_id()
    response = requests.get(f'https://api.trello.com/1/boards/{trello_board_id}/lists?key={trello_auth_cred[0]}&token={trello_auth_cred[1]}')
    
    all_lists = response.json()

    for i in all_lists:
        if i['name'] == list_name:
            list_id = i['id']
    
    return list_id

def get_trello_cards():
    trello_auth_cred = get_trello_credentials()
    trello_board_id = get_trello_board_id()
    response = requests.get(f'https://api.trello.com/1/boards/{trello_board_id}/cards?key={trello_auth_cred[0]}&token={trello_auth_cred[1]}')

    card_list = []
    for card in response.json():
        existing_card = TrelloCard(card['id'], card['name'], card['idList'])

        card_list.append(existing_card)

    return card_list

def move_trello_card(card_id, new_list_id):
    trello_auth_cred = get_trello_credentials()
    requests.put(f'https://api.trello.com/1/cards/{card_id}?key={trello_auth_cred[0]}&token={trello_auth_cred[1]}&idList={new_list_id}')

def create_trello_card(new_card):
    trello_auth_cred = get_trello_credentials()
    trello_list_id = get_trello_list_id("To Do")
    requests.post(f'https://api.trello.com/1/cards/?key={trello_auth_cred[0]}&token={trello_auth_cred[1]}&idList={new_card.idList}&name={new_card.name}')


def archive_trello_card(card_id):
    trello_auth_cred = get_trello_credentials()
    requests.put(f'https://api.trello.com/1/cards/{card_id}?key={trello_auth_cred[0]}&token={trello_auth_cred[1]}&closed=true')

 
    

