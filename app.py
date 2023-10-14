# flask_app/app.py

from flask import Flask

app = Flask(__name__)


@app.route('/')
def my_index_view():
    return 'Это мой первый Flask-проект'


if __name__ == '__main__':
    app.run()