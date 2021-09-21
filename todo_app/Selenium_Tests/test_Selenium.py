import os, pytest, dotenv
from threading import Thread
from todo_app.data.todo_items import create_test_db, delete_test_db
from todo_app import app
from selenium import webdriver 
from selenium.webdriver.support.ui import Select


@pytest.fixture(scope='module')
def app_with_temp_board():
    file_path = dotenv.find_dotenv('.env')
    dotenv.load_dotenv(file_path, override=True)
    
    db_name = create_test_db('test_todo_app')
    os.environ['MONGO_DB_NAME'] = db_name

    application = app.create_app()
    
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app
    
    thread.join(1)
    delete_test_db(db_name)

@pytest.fixture(scope="module")
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=opts) as driver:
        yield driver

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://127.0.0.1:5000')
    
    assert driver.title == 'To-Do App'
    driver.find_element_by_name("new_item_title").send_keys('Test_New')
    driver.find_element_by_name("new_item_description").send_keys('Test Description')
    driver.find_element_by_name("new_task_submit").click()

    assert driver.find_element_by_xpath("//*[starts-with(@id, 'Todo_')]")
    driver.find_element_by_xpath("//*[starts-with(@action, '/Doing')]")
    driver.find_element_by_xpath("//*[starts-with(@id, 'move_item_')]").submit()
    
    assert driver.find_element_by_xpath("//*[starts-with(@id, 'Doing')]")
    driver.find_element_by_xpath("//*[starts-with(@action, '/Done')]")
    driver.find_element_by_xpath("//*[starts-with(@id, 'toggle_item_')]").submit()
 