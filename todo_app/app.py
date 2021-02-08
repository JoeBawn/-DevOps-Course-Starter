from flask import Flask, render_template, request, redirect
from operator import itemgetter

from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, get_item, add_item, save_item, remove_item
from todo_app.data.trello_items import get_trello_credentials, get_trello_board_id, get_trello_cards, get_trello_list_id, get_trello_lists_on_board, create_trello_card, TrelloCard, move_trello_card, archive_trello_card

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():

    trello_list_id = {}
    trello_list_id['To Do'] = get_trello_list_id('To Do')
    trello_list_id['In Progress'] = get_trello_list_id('In Progress')
    trello_list_id['Completed'] =get_trello_list_id('Completed')

    all_lists = get_trello_lists_on_board()

    items = get_trello_cards()
    if request.values.get('sort') == '1':
        items.sort(key=lambda x: x.idList)
    elif request.values.get('sort') == '2':
        items.sort(key=lambda x: x.idList, reverse=True)
    return render_template("index.html",items=items,lists=all_lists)

@app.route('/new_item', methods=['POST'])
def new_item():
    new_item_title = request.form.get('new_item_title')
    trello_default_list = get_trello_list_id('To Do')
    
    new_card = TrelloCard(0, new_item_title, trello_default_list)
    create_trello_card(new_card)
    return redirect(request.headers.get('Referer'))

@app.route('/archive_item', methods=['POST'])
def remove_existing_item():
    trello_list_id = {}
    trello_list_id['To Do'] = get_trello_list_id('To Do')
    trello_list_id['In Progress'] = get_trello_list_id('In Progress')
    trello_list_id['Completed'] =get_trello_list_id('Completed')
    allcards = get_trello_cards()
    all_lists = get_trello_lists_on_board()
    
    toggle_item = request.form.get('archive_id')

    for card in allcards:
        if card.id == toggle_item:
            
            archive_trello_card(card.id)
    
    return redirect(request.headers.get('Referer'))


@app.route('/toggle_status', methods=['POST'])
def toggle_status():
    trello_list_id = {}
    trello_list_id['To Do'] = get_trello_list_id('To Do')
    trello_list_id['In Progress'] = get_trello_list_id('In Progress')
    trello_list_id['Completed'] =get_trello_list_id('Completed')
    
    allcards = get_trello_cards()
    all_lists = get_trello_lists_on_board()
    
    toggle_item = request.form.get('item_id')

    for card in allcards:
        if card.id == toggle_item:
            new_list_id = trello_list_id['Completed']
            move_trello_card(card.id, new_list_id)
        elif card.id == toggle_item:
            new_list_id = trello_list_id['In Progress']
            move_trello_card(card.id, new_list_id)
    
    return redirect(request.headers.get('Referer'))


if __name__ == '__main__':
    app.run()
