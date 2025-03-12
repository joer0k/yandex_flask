import json
import os
from random import choice

from flask import Flask, render_template, redirect, request, url_for
from flask_wtf import *
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
