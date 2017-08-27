from flask import Flask
from flask_script import Manager

app= Flask(__name__)
# flask script runserver, shell 실행 확장
manager = Manager(app)

@app.route('/')
def index():
    return '<h1>hello flask world</h1>'

@app.route('/profile/<int:id>/')
def profile():
    return '<h1>profile</h1>'


if __name__ =='__main__':
    manager.run()