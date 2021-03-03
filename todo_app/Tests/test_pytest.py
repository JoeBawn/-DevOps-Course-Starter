import datetime, pytest
from todo_app.data.trello_items import TrelloCard, ViewModel

@pytest.fixture
def test_card_list():
    today = datetime.date.today()
    all_cards = [
        TrelloCard(1,"Test Card 1",1001,today,"Test Description 1",today - datetime.timedelta(days=8)),
        TrelloCard(2,"Test Card 2",1002,today - datetime.timedelta(days=2),"Test Description 2", today - datetime.timedelta(days=7)),
        TrelloCard(3,"Test Card 3",1003,today - datetime.timedelta(days=3),"Test Description 3", today - datetime.timedelta(days=6)),
        TrelloCard(4,"Test Card 4",1001,today - datetime.timedelta(days=4),"Test Description 4", today),
        TrelloCard(5,"Test Card 5",1001,today,"Test Description 5", today - datetime.timedelta(days=4)),
        TrelloCard(6,"Test Card 6",1002,today - datetime.timedelta(days=6),"Test Description 6", today - datetime.timedelta(days=3)),
        TrelloCard(7,"Test Card 7",1003,today - datetime.timedelta(days=7),"Test Description 7", today - datetime.timedelta(days=2)),
        TrelloCard(8,"Test Card 8",1003,today - datetime.timedelta(days=8),"Test Description 8", today)
    ]
    return all_cards
 
@pytest.fixture
def list_ids():
    trello_list_ids = {"todo": 1001, "inprogress": 1002, "complete": 1003}
    return trello_list_ids

class Trello_Test():
 
    @staticmethod
    def test_todo_items(test_card_list, list_ids):
        todo_list_id = list_ids['todo']
        view_model = ViewModel(test_card_list, list_ids)
        
        all_todo_items = view_model.todo
 
        for card in all_todo_items:
            assert card.idList == todo_list_id

    @staticmethod
    def test_inprogress(test_card_list, list_ids):        

        todo_list_id = trello_list_ids['inprogress']
        view_model = ViewModel(test_card_list, list_ids)

        inprogress_items = view_model.inprogress_items

        for i in inprogress_items:
            assert todo_list_id == i.idList
    
    @staticmethod
    def test_complete(test_card_list, list_ids):        

        todo_list_id = trello_list_ids['complete']
        view_model = ViewModel(test_card_list, list_ids)

        complete_items = view_model.complete_items

        for i in complete_items:
            assert todo_list_id == i.idList

    @staticmethod
    def test_recent_complete_items(test_card_list, list_ids):        

        view_model = ViewModel(test_card_list, list_ids)

        recent_complete_items = view_model.recent_complete_items
        
        assert len(recent_complete_items) == 2

    @staticmethod
    def test_older_complete_items(test_card_list, list_ids):        

        view_model = ViewModel(test_card_list, list_ids)

        older_complete_items = view_model.older_complete_items

        assert len(older_complete_items) == 3