import json
import os
from datetime import datetime
from random import choice
from data.register_form import RegisterForm
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager
from flask_wtf import *
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from data import db_session
from data.jobs import Jobs
from data.users import User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'joerok_secret_key'


class LoginForm(FlaskForm):
    username = StringField('id астронавта ', validators=[DataRequired()])
    password = PasswordField('Пароль астронавта ', validators=[DataRequired()])
    username_k = StringField('id капитана', validators=[DataRequired()])
    password_k = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Войти')


@app.route('/<title>')
@app.route('/index/<title>')
def first(title):
    return render_template('base.html', title=title)


@app.route('/training/<prof>')
def profession(prof):
    return render_template('training.html', prof=prof)


@app.route('/list_prof/<lst>')
def list_prof(lst):
    professions = [
        "Веб-разработчик",
        "Аналитик данных",
        "Разработчик искусственного интеллекта",
        "Автоматизатор тестирования",
        "DevOps-инженер",
        "Frontend-разработчик",
        "Инженер данных",
        "Инженер надежности сайта",
        "Программист",
        "Python-разработчик",
        "Java-разработчик",
        "Графический дизайнер"
    ]
    return render_template('list_prof.html', list=lst, professions=professions)


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    dict_answer = {
        'title': 'Анкета',
        'surname': 'Watny',
        'name': 'Mark',
        'education': 'выше среднего',
        'profession': 'штурман марсохода',
        'sex': 'male',
        'motivation': 'Всегда мечтал застрять на Марсе!',
        'ready': True
    }
    return render_template('auto_answer.html', dict_answer=dict_answer)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Аварийный доступ', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/distribution')
def distribution():
    names = [
        "Джон Смит",
        "Эмили Джонсон",
        "Майкл Дэвис",
        "Сара Томпсон",
        "Дэвид Уильямс",
        "Джессика Браун",
        "Ричард Уилсон",
        "Лаура Мур",
        "Кристофер Тейлор",
        "Аманда Андерсон"
    ]
    return render_template('distribution.html', data=names)


@app.route('/table/<sex>/<age>')
def table(sex, age):
    return render_template('table.html', sex=sex, age=int(age))


@app.route('/galery', methods=['GET', 'POST'])
def galery():
    files = os.listdir('static/img/galery')
    if request.method == 'POST' and request.files['file']:
        f = request.files['file']
        f.save(f'static/img/galery/{f.filename}')
        return redirect('/galery')
    return render_template('galery.html', photos=files)


@app.route('/member')
def member():
    with open('templates/members.json', 'r', encoding='utf-8') as file_json:
        data = json.load(file_json)
    member = choice(data['crew_members'])
    member['specialities'] = sorted(member['specialities'])
    return render_template('member.html', member=member)


@app.route('/')
def works_log():
    data_jobs = []
    data_leaders = {}
    db_session.global_init(f"db/mars.db")
    session = db_session.create_session()
    for job in session.query(Jobs).all():
        data_jobs.append([job.job, job.team_leader, job.work_size, job.collaborators, job.is_finished])
        data_leaders[job.team_leader] = f'{job.user.surname} {job.user.name}'
    return render_template('works_log.html', data=data_jobs, data_leaders=data_leaders)

#регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_repeat.data:
            return render_template('register.html', form=form, message='Пароли не совпадают')
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form, message='Пользователь с такой почтой уже существует')
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data

        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('register.html', form=form)


if __name__ == '__main__':
    db_session.global_init('db/mars.db')
    app.run(port=8080, host='127.0.0.1', debug=True)
