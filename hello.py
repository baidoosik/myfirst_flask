from flask import Flask,render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import form

app= Flask(__name__)
# flask script runserver, shell 실행 확장
manager = Manager(app)
#flask-bootstrap 적용
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile/')
def profile():
    #user_id =profile_id
    return render_template('profile.html')

#404, 500 page

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

if __name__ =='__main__':
    manager.run()