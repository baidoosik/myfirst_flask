from flask import Flask

app= Flask(__name__)

@app.route('/')
def index():
    return '<h1>hello flask world'


if __name__ =='__main__'