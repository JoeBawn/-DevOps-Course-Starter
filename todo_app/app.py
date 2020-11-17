from flask import Flask, render_template

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index(name=None):
    return render_template("index.html",name=name)


if __name__ == '__main__':
    app.run()
