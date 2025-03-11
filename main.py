from flask import Flask, render_template, redirect
from flask_wtf import *
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)


@app.route('/<title>')
@app.route('/index/<title>')
def first(title):
    return render_template('base.html', title=title)


@app.route('/training/<prof>')
def profession(prof):
    return render_template('training.html', prof=prof)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
