from flask import Flask, request, render_template, redirect
from login import LoginForm
from register import RegistrationForm
from data import db_session
from data.users import User
import cassiopeia as cass

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
cass.set_riot_api_key("RGAPI-d8b0420d-7d54-4e07-9128-1fcfdb74bf51")
cass.set_default_region("RU")


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        session = db_session.create_session()
        if session.query(User).filter(User.email == email).first():
            return render_template('register.html',
                                   form=form,
                                   message="Адрес почты занят!")
        if session.query(User).filter(User.name == username).first():
            return render_template('register.html',
                                   form=form,
                                   message="Логин занят!")
        user = User(
            name=username,
            email=email,
        )
        user.set_password(password)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/search', methods=['POST', 'GET'])
def search():
    summoner_name = request.form.get('summoner_name')
    summoner = cass.get_summoner(name=summoner_name)
    name = summoner.name
    level = summoner.level
    region = summoner.region
    return render_template('search.html', name=name, level=level, region=region)


if __name__ == '__main__':
    db_session.global_init("db/data.sqlite")
    app.run(host='127.0.0.1', port='8080', debug=True)
