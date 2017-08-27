import json
from flask import Flask,render_template,redirect,session,url_for,flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Email,Required


with open('envs.json','r') as f:
    envs = json.loads(f.read())

app= Flask(__name__)
app.config['SECRET_KEY']=envs['csrf_key']
# flask script runserver, shell 실행 확장
manager = Manager(app)
#flask-bootstrap 적용
bootstrap = Bootstrap(app)

class NameForm(FlaskForm):
    name= StringField('what is your naem?',validators=[Required()])
    email = StringField('what is your e-mail?',validators=[Required(),Email()])
    submit =SubmitField('Submit')

@app.route('/',methods=['GET','POST'])
def index():
    form =NameForm()

    if form.validate_on_submit():
        old_name = session['name']

        if old_name is not None and old_name !=form.name.data:
            flash('사용자가 변경되었습니다.')
        session['name']= form.name.data
        session['email'] = form.email.data

        return redirect(url_for('index')) #post/rediret/get patter 기법. 마지막 요청을 post로 남기지 않기 위해.

    return render_template('index.html',form=form,name=session['name'])
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