import os
import json
from flask import Flask,render_template,redirect,session,url_for,flash
from flask_script import Manager,Shell
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField,SubmitField
from wtforms.validators import Email,Required

basedir = os.path.abspath(os.path.dirname(__file__))

with open('envs.json','r') as f:
    envs = json.loads(f.read())

app= Flask(__name__)
app.config['SECRET_KEY']=envs['csrf_key']
app.config['SQLALCHEMY_DATABASE_URI']=\
    'sqlite:///'+ os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =True

# flask app과 db 연결
db = SQLAlchemy(app)
# flask script runserver, shell 실행 확장
manager = Manager(app)
#flask-bootstrap 적용
bootstrap = Bootstrap(app)

# shell에 db import 자동 반영
def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)

manager.add_command("shell",Shell(make_context=make_shell_context))

# model 정의
class Role(db.Model):
    __tablename__ = 'roles'
    id =  db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role')

    def __repr__(self):
        return '<Role {}>'.format(self.name)

class User(db.Model):
    __tablename__ = 'users'
    id= db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(40),unique=True,index=True)
    email = db.Column(db.String(60))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<USER {}>'.format(self.user_name)

# form 정의
class NameForm(FlaskForm):
    name= StringField('what is your name?',validators=[Required()])
    email = StringField('what is your e-mail?',validators=[Required(),Email()])
    submit =SubmitField('Submit')

@app.route('/',methods=['GET','POST'])
def index():
    form =NameForm()

    if form.validate_on_submit():
        name = User.query.filter_by(user_name=form.name.data).first()

        if name is None:
            #새로운 사용자 db에 추가
            flash('db에 사용자가 추가되었습니다.')
            user = User(user_name=form.name.data,email=form.email.data)
            db.session.add(user)
            session['known']=False
        else:
            session['known']=True

        session['name']= form.name.data
        session['email'] = form.email.data
        form.name.data=''
        form.email.data=''

        return redirect(url_for('index')) #post/rediret/get patter 기법. 마지막 요청을 post로 남기지 않기 위해.

    return render_template('index.html',form=form,name=session['name'],
                           known=session.get('known',False))
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