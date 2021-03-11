import os, pytest, dotenv
from threading import Thread
from todo_app.data.trello_items import create_trello_board, delete_trello_board
from todo_app import app
from selenium import webdriver 
from selenium.webdriver.support.ui import Select


@pytest.fixture(scope='module')
def app_with_temp_board():
    board_id = create_trello_board('Test_Board')
    file_path = dotenv.find_dotenv('.env')
    dotenv.load_dotenv(file_path)
    os.environ['TRELLO_API_BOARD_ID'] = board_id

    application = app.create_app()
    
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    
    thread.join(1)
    delete_trello_board(board_id)

@pytest.fixture(scope="module")
def driver():
    with webdriver.Edge(("C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe")) as driver:
        yield driver

def test_task_journey(driver, app_with_temp_board):
    # msedgedriver.exe is downloaded and placed in the browser directory
    driver.get('http://127.0.0.1:5000')
    assert driver.title == 'To-Do App'
    
    driver.find_element_by_name("new_item_title").send_keys('Test Name')
    driver.find_element_by_name("new_item_desc").send_keys('Test Description')
    driver.find_element_by_name("submit").click()

    assert driver.find_element_by_xpath("//*[starts-with(@id, 'Todo')]")
    
    select = Select(driver.find_element_by_xpath("//*[starts-with(@id, 'toggle_item_')]"))
    select.select_by_index(2)
    driver.find_element_by_xpath("//*[starts-with(@id, 'toggle_item_')]").submit()
    
    assert driver.find_element_by_xpath("//*[starts-with(@id, 'InProgress')]")

    select = Select(driver.find_element_by_xpath("//*[starts-with(@id, 'toggle_item_')]"))
    select.select_by_index(3)
    driver.find_element_by_xpath("//*[starts-with(@id, 'toggle_item_')]").submit()
    
    assert driver.find_element_by_xpath("//*[starts-with(@id, 'Completed')]")