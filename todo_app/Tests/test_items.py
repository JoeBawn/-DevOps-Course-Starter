import datetime,pytest
from todo_app.data.trello_items import ToDoCard, ViewModel

@pytest.fixture
def card_list():
    card_list = [
            ToDoCard(1, 'Test Card 1', 1001, datetime.date.today() + datetime.timedelta(-8), 'Test Description 1', datetime.date.today() + datetime.timedelta(-8)),
            ToDoCard(2, 'Test Card 2', 1002, datetime.date.today() + datetime.timedelta(-7), 'Test Description 2', datetime.date.today() + datetime.timedelta(-7)),
            ToDoCard(3, 'Test Card 3', 1003, datetime.date.today() + datetime.timedelta(-6), 'Test Description 3', datetime.date.today() + datetime.timedelta(-2)),
            ToDoCard(4, 'Test Card 4', 1003, datetime.date.today() + datetime.timedelta(-6), 'Test Description 4', datetime.date.today() + datetime.timedelta(-3)),
            ToDoCard(5, 'Test Card 5', 1003, datetime.date.today() + datetime.timedelta(-5), 'Test Description 5', datetime.date.today() + datetime.timedelta(-2)),
            ToDoCard(6, 'Test Card 6', 1001, datetime.date.today() + datetime.timedelta(-4), 'Test Description 6', datetime.date.today() + datetime.timedelta(-2)),
            ToDoCard(7, 'Test Card 7', 1003, datetime.date.today() + datetime.timedelta(-3), 'Test Description 7', datetime.date.today()),
            ToDoCard(8, 'Test Card 8', 1003, datetime.date.today() + datetime.timedelta(-1), 'Test Description 8', datetime.date.today())
        ]
    return card_list

@pytest.fixture
def list_ids():
    list_ids = {'ToDo':1001,'Doing':1002,'Done':1003}
    return list_ids

class TestToDo:

    @staticmethod
    def test_get_todo(card_list,list_ids):        

        todo_list_id = list_ids['ToDo']
        view_model = ViewModel(card_list, list_ids)

        items_todo = view_model.items_todo

        for i in items_todo:
            assert todo_list_id == i.idList
        
    @staticmethod
    def test_get_doing(card_list,list_ids):        

        todo_list_id = list_ids['Doing']
        view_model = ViewModel(card_list, list_ids)

        items_doing = view_model.items_doing

        for i in items_doing:
            assert todo_list_id == i.idList
    
    @staticmethod
    def test_get_done(card_list,list_ids):        

        todo_list_id = list_ids['Done']
        view_model = ViewModel(card_list, list_ids)

        items_done = view_model.items_done

        for i in items_done:
            assert todo_list_id == i.idList

    @staticmethod
    def test_recent_done_items(card_list,list_ids):        

        view_model = ViewModel(card_list, list_ids)

        recent_done_items = view_model.recent_done_items
        
        assert len(recent_done_items) == 2

    @staticmethod
    def test_older_done_items(card_list,list_ids):        

        view_model = ViewModel(card_list, list_ids)

        older_done_items = view_model.older_done_items

        assert len(older_done_items) == 3