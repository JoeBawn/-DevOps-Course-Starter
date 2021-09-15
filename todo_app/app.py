from flask import Flask, render_template, request, redirect
from operator import itemgetter
import pytest, datetime

from todo_app.flask_config import Config
from todo_app.data.trello_items import ToDoCard, ViewModel, get_trello_credentials, get_trello_board_id, get_trello_cards, get_trello_list_id, get_trello_lists_on_board, create_trello_card, move_trello_card, delete_trello_card, get_trello_card_list, get_todo_cards, move_todo_card, create_todo_card, delete_todo_card

def create_app():  
    app = Flask(__name__)
    

    # All the routes and setup code etc

    @app.route('/')
    def index():

        items = get_todo_cards()
        lists = {'ToDo':'todo','Doing':'doing','Done':'done'}

        get_view_model = ViewModel(items, lists)

        todays_date = datetime.datetime.strftime(datetime.date.today(), '%d/%m/%Y')

        if request.values.get('sort') == '1':
            items.sort(key=lambda x: x.due_date)
        elif request.values.get('sort') == '2':
            items.sort(key=lambda x: x.due_date, reverse=True)
        return render_template("index.html",View_Model=get_view_model, todays_date=todays_date)

    @app.route('/new_item', methods=['POST'])
    def new_item():
        new_item_title = request.form.get('new_item_title')
        default_list = 'todo'
        if request.form.get('new_item_due'):
            due_date = datetime.datetime.strptime(request.form.get('new_item_due'), '%Y-%m-%d')
        else:
            due_date = datetime.datetime.today() + datetime.timedelta(30)
        
        description = request.form.get('new_item_description')
        
        new_card = ToDoCard(0, new_item_title, default_list, due_date, description, datetime.datetime.today())
        create_todo_card(new_card)
        return redirect(request.headers.get('Referer'))

    @app.route('/remove_item', methods=['POST'])
    def remove_existing_item():
        allcards = get_todo_cards()
        lists = {'todo':'todo','doing':'doing','done':'done'}
        
        toggle_item = request.form.get('delete_id')

        for card in allcards:
            if toggle_item == str(card.id):
                delete_todo_card(card.id)
        
        return redirect(request.headers.get('Referer'))


    @app.route('/Doing', methods=['POST'])
    def in_progress():
        allcards = get_todo_cards()
        lists = {'todo':'todo','doing':'doing','done':'done'}

        toggle_item = request.form.get('item_id')

        for card in allcards:
            if toggle_item == str(card.id):
                for l in lists:
                    if l == "doing":
                        desired_list_id = l
                        move_todo_card(card.id, desired_list_id)
        
        return redirect(request.headers.get('Referer'))

    @app.route('/Done', methods=['POST'])
    def Done():
        allcards = get_todo_cards()
        lists = {'todo':'todo','doing':'doing','done':'done'}

        toggle_item = request.form.get('item_id')

        for card in allcards:
            if toggle_item == str(card.id):
                for l in lists:
                    if l == "done":
                        desired_list_id = l
                        move_todo_card(card.id, desired_list_id)
        return redirect(request.headers.get('Referer'))


    if __name__ == '__main__':
        app.run()

    return app
