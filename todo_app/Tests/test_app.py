import os, pytest, json, datetime
import todo_app.app
import dotenv
import mongomock 
import pymongo

@pytest.fixture
def client():
    file_path = dotenv.find_dotenv('.env.test') 
    dotenv.load_dotenv(file_path, override=True) 
    with mongomock.patch(servers=(('testmongo.com', 27017),)):
        test_app = todo_app.app.create_app()  
        with test_app.test_client() as client:
            yield client

def test_index_page(client):
    
    response = client.get('/')

    assert b'To Do' in response.data
    assert b'Doing' in response.data

@mongomock.patch(servers=(('testmongo.com', 27017),))
def test_add_item():
    db_connection = os.getenv('MONGO_URL')
    db_name = os.getenv('MONGO_DB_NAME')
    connection = pymongo.MongoClient(db_connection)
    db = connection[db_name]
    item = {"Test1" : "Test2"}
    collection = db['test_col']
    collection.insert_one(item)