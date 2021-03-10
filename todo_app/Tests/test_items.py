import datetime,pytest
from todo_app.data.trello_items import TrelloCard, ViewModel

@pytest.fixture
def card_list():
    card_list = [
            TrelloCard(1, 'Test Card 1', 1001, datetime.date.today() + datetime.timedelta(-8), 'Test Description 1', datetime.date.today() + datetime.timedelta(-8)),
            TrelloCard(2, 'Test Card 2', 1002, datetime.date.today() + datetime.timedelta(-7), 'Test Description 2', datetime.date.today() + datetime.timedelta(-7)),
            TrelloCard(3, 'Test Card 3', 1003, datetime.date.today() + datetime.timedelta(-6), 'Test Description 3', datetime.date.today() + datetime.timedelta(-2)),
            TrelloCard(4, 'Test Card 4', 1003, datetime.date.today() + datetime.timedelta(-6), 'Test Description 4', datetime.date.today() + datetime.timedelta(-3)),
            TrelloCard(5, 'Test Card 5', 1003, datetime.date.today() + datetime.timedelta(-5), 'Test Description 5', datetime.date.today() + datetime.timedelta(-2)),
            TrelloCard(6, 'Test Card 6', 1001, datetime.date.today() + datetime.timedelta(-4), 'Test Description 6', datetime.date.today() + datetime.timedelta(-2)),
            TrelloCard(7, 'Test Card 7', 1003, datetime.date.today() + datetime.timedelta(-3), 'Test Description 7', datetime.date.today()),
            TrelloCard(8, 'Test Card 8', 1003, datetime.date.today() + datetime.timedelta(-1), 'Test Description 8', datetime.date.today())
        ]
    return card_list

@pytest.fixture
def trello_list_ids():
    trello_list_ids = {'ToDo':1001,'InProgress':1002,'Completed':1003}
    return trello_list_ids

class TestTrello:

    @staticmethod
    def test_get_todo(card_list,trello_list_ids):        

        todo_list_id = trello_list_ids['ToDo']
        view_model = ViewModel(card_list, trello_list_ids)

        items_todo = view_model.items_todo

        for i in items_todo:
            assert todo_list_id == i.idList
        
    @staticmethod
    def test_get_inprogress(card_list,trello_list_ids):        

        todo_list_id = trello_list_ids['InProgress']
        view_model = ViewModel(card_list, trello_list_ids)

        items_inprogress = view_model.items_inprogress

        for i in items_inprogress:
            assert todo_list_id == i.idList
    
    @staticmethod
    def test_get_completed(card_list,trello_list_ids):        

        todo_list_id = trello_list_ids['Completed']
        view_model = ViewModel(card_list, trello_list_ids)

        items_completed = view_model.items_completed

        for i in items_completed:
            assert todo_list_id == i.idList

    @staticmethod
    def test_recent_completed_items(card_list,trello_list_ids):        

        view_model = ViewModel(card_list, trello_list_ids)

        recent_completed_items = view_model.recent_completed_items
        
        assert len(recent_completed_items) == 2

    @staticmethod
    def test_older_completed_items(card_list,trello_list_ids):        

        view_model = ViewModel(card_list, trello_list_ids)

        older_completed_items = view_model.older_completed_items

        assert len(older_completed_items) == 3