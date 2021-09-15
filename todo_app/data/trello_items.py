import os 
import requests, datetime, json
import pymongo

class ToDoCard:
    def __init__(self, id, name, idList, due_date, description, modified):
        self.id = id
        self.name = name
        self.idList = idList
        self.due_date = due_date
        self.description = description
        self.modified = modified
    
    def get_date(self):
        return datetime.datetime.strftime(self.due_date, '%Y-%m-%d')
    
    def get_user_date(self):
        return datetime.datetime.strftime(self.due_date, '%d/%m/%Y')

    def get_modified_date(self):
        return datetime.datetime.strftime(self.modified, '%Y-%m-%d')
    
    def get_modified_user_date(self):
        return datetime.datetime.strftime(self.modified, '%d/%m/%Y')
    
    def get_card_as_dictionary(self):
        return {'name' : self.name, 'idList' : self.idList, 'due_date' : self.due_date, 'description' : self.description, 'modified' : self.modified}

class ViewModel:
    def __init__(self, items, lists):
        self._items = items
        self._lists = lists

    @property
    def items(self):
        return self._items

    @property
    def lists(self):
        return self._lists

    @property
    def items_todo(self):
        items = []
        for item in self._items:
            if item.idList == self.lists['ToDo']:
                items.append(item)
        return items

    @property
    def items_doing(self):
        items = []
        for item in self._items:
            if item.idList == self.lists['Doing']:
                items.append(item)
        return items

    @property
    def items_done(self):
        items = []
        for item in self._items:
            if item.idList == self.lists['Done']:
                items.append(item)
        return items

    @property
    def recent_done_items(self):
        items = []
        for item in self._items:
            if item.idList == self.lists['Done'] and item.modified == datetime.date.today():
                items.append(item)
        return items

    @property
    def older_done_items(self):
        items = []
        for item in self._items:
            if item.idList == self.lists['Done'] and item.modified != datetime.date.today():
                items.append(item)
        return items

def get_mongodb_connection():
    mongodb_url = os.getenv('MONGO_URL')
    return mongodb_url

def get_mongodb_database_name():
    mongodb_name = os.getenv('MONGO_DB_NAME')
    return mongodb_name

def mongo_db_connection():
    db_connection = get_mongodb_connection()
    db_name = get_mongodb_database_name()

    mongo_client = pymongo.MongoClient(db_connection)
    db = mongo_client[db_name]

    return db

def get_todo_cards():
    db = mongo_db_connection()
    collections = db.list_collection_names()

    card_list = []
    for col in collections:
        collection = db[col]

        for card in collection.find({}):
            card_list.append(ToDoCard(card['_id'], card['name'], card['idList'], card['due_date'], card['description'], card['modified']))

    return card_list

def move_todo_card(card_id, new_list_id):
    db = mongo_db_connection()
    collections = db.list_collection_names()

    for col in collections:
        collection = db[col]
        for card in collection.find({}): 
            if str(card['_id']) == str(card_id):
                new_card = ToDoCard(0, card['name'], new_list_id, card['due_date'], card['description'], datetime.datetime.today())
                new_collection = db[new_list_id]
                new_collection.insert_one(new_card.get_card_as_dictionary())
                result = collection.delete_one({'_id' : card['_id']})
                print(result)
                break

def delete_todo_card(card_id):
    db = mongo_db_connection()
    collections = db.list_collection_names()

    for col in collections:
        collection = db[col]
        for card in collection.find({}): 
            if str(card['_id']) == str(card_id):
                result = collection.delete_one({'_id' : card_id})

def create_todo_card(new_card):
    db = mongo_db_connection()
    card = new_card.get_card_as_dictionary()
    db['todo'].insert_one(card)

def create_test_db(db_name):
    db_connection = get_mongodb_connection()
    mongo_client = pymongo.MongoClient(db_connection)
    db = mongo_client[db_name]
    db['todo']
    db['doing']
    db['done']

    return db_name

def delete_test_db(db_name):
    db_connection = get_mongodb_connection()
    mongo_client = pymongo.MongoClient(db_connection)
    mongo_client.drop_database(db_name)

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
        if card['due'] == None:
            due_date = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(365), '%Y-%m-%dT%H:%M:%S.%fZ')

        else:
            due_date = card['due']

        card_list.append(TrelloCard(card['id'], card['name'], card['idList'], datetime.datetime.strptime(due_date, '%Y-%m-%dT%H:%M:%S.%fZ'), card['desc'], datetime.datetime.strptime(card['dateLastActivity'], '%Y-%m-%dT%H:%M:%S.%fZ').date()))
        
    return card_list

def get_trello_card_list(listid):
    trello_auth_cred = get_trello_credentials()
    lists = get_trello_lists_on_board()
    for _list in lists:
        if _list['id'] == listid:
            required_list_id = _list['id']
    response = requests.get(f'https://api.trello.com/1/lists/{required_list_id}/cards?key={trello_auth_cred[0]}&token={trello_auth_cred[1]}')

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
    requests.post(f'https://api.trello.com/1/cards/?key={trello_auth_cred[0]}&token={trello_auth_cred[1]}&idList={new_card.idList}&name={new_card.name}&desc={new_card.description}&due={new_card.get_date()}')


def delete_trello_card(card_id):
    trello_auth_cred = get_trello_credentials()
    requests.delete(f'https://api.trello.com/1/cards/{card_id}?key={trello_auth_cred[0]}&token={trello_auth_cred[1]}&closed=true')

def create_trello_board(board_name):
    trello_auth_cred = get_trello_credentials()
    response = requests.post(f'https://api.trello.com/1/boards/?key={trello_auth_cred[0]}&token={trello_auth_cred[1]}&name={board_name}')
    new_board = response.json()
    return new_board['id']

def delete_trello_board(board_id):
    trello_auth_cred = get_trello_credentials()
    requests.delete(f'https://api.trello.com/1/boards/{board_id}/?key={trello_auth_cred[0]}&token={trello_auth_cred[1]}')
 
    

