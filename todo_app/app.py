from flask import Flask, render_template, request, redirect
from operator import itemgetter
import pytest, datetime, os, requests, json
from flask_login import LoginManager, login_required, login_user, current_user
from oauthlib.oauth2 import WebApplicationClient
from todo_app.user import User

from todo_app.flask_config import Config
from todo_app.data.todo_items import ToDoCard, ViewModel, get_todo_cards, move_todo_card, create_todo_card, delete_todo_card


login_manager = LoginManager()

@login_manager.unauthorized_handler
def unauthenticated():
    github_client =  WebApplicationClient(os.environ.get('CLIENTID'))
    github_redirect = github_client.prepare_request_uri("https://github.com/login/oauth/authorize")

    return redirect(github_redirect) 

@login_manager.user_loader
def load_user(github_user):
    
    return User(github_user)


def create_app():  
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['LOGIN_DISABLED'] = os.environ.get('LOGIN_DISABLED', 'False').lower() in ['true', '1']
    login_manager.init_app(app)
    

    # All the routes and setup code etc

    @app.route('/')
    @login_required
    def index():

        items = get_todo_cards()
        lists = {'ToDo':'todo','Doing':'doing','Done':'done'}

        get_view_model = ViewModel(items, lists)

        todays_date = datetime.datetime.strftime(datetime.date.today(), '%d/%m/%Y')

        if request.values.get('sort') == '1':
            items.sort(key=lambda x: x.due_date)
        elif request.values.get('sort') == '2':
            items.sort(key=lambda x: x.due_date, reverse=True)

        if not app.config['LOGIN_DISABLED']:
            if current_user.role == 'writer':
                return render_template("index.html",View_Model=get_view_model, todays_date=todays_date)
            elif current_user.role == 'reader':
                return render_template('index_read.html', View_Model=get_view_model, todays_date=todays_date)
            else:
                return render_template('index_read.html', View_Model=get_view_model, todays_date=todays_date)
        else:
            return render_template('index.html', View_Model=get_view_model, todays_date=todays_date)


    @app.route('/new_item', methods=['POST'])
    @login_required
    def new_item():
        if 'LOGIN_DISABLED' in app.config or current_user.role == 'writer':

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
    @login_required
    def remove_existing_item():
        if 'LOGIN_DISABLED' in app.config or current_user.role == 'writer':
            allcards = get_todo_cards()
            lists = {'todo','doing','done'}
            
            toggle_item = request.form.get('delete_id')

            for card in allcards:
                if toggle_item == str(card.id):
                    delete_todo_card(card.id)
        
        return redirect(request.headers.get('Referer'))


    @app.route('/Doing', methods=['POST'])
    @login_required
    def in_progress():
        if 'LOGIN_DISABLED' in app.config or current_user.role == 'writer':
            allcards = get_todo_cards()
            lists = {'todo','doing','done'}

            toggle_item = request.form.get('item_id')

            for card in allcards:
                if toggle_item == str(card.id):
                    move_todo_card(card.id, 'doing')
        
        return redirect(request.headers.get('Referer'))

    @app.route('/Done', methods=['POST'])
    @login_required
    def Done():
        if 'LOGIN_DISABLED' in app.config or current_user.role == 'writer':
            allcards = get_todo_cards()
            lists = {'todo','doing','done'}

            toggle_item = request.form.get('item_id')

            for card in allcards:
                if toggle_item == str(card.id):
                    move_todo_card(card.id, 'done')
        return redirect(request.headers.get('Referer'))

    @app.route('/login')
    def login_callback():
        callback_code = request.args.get("code")
        github_client =  WebApplicationClient(os.environ.get('CLIENTID'))
        github_token = github_client.prepare_token_request("https://github.com/login/oauth/access_token", code=callback_code) 
        github_access = requests.post(github_token[0], headers=github_token[1], data=github_token[2], auth=(os.environ.get('CLIENTID'), os.environ.get('CLIENTSECRET')))
        github_json = github_client.parse_request_body_response(github_access.text)
        github_user_request_param = github_client.add_token("https://api.github.com/user")
        github_user = requests.get(github_user_request_param[0], headers=github_user_request_param[1]).json()
        
        login_user(User(github_user))

        return redirect('/') 


    if __name__ == '__main__':
        app.run()
        

    return app
