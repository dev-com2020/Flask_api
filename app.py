from flask import Flask
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import click
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'S_U_perS3crEt_KEY#9999'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.app_context()


class Data(db.Model):
    passengerId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    survived = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), default=None)
    age = db.Column(db.Integer, default=-1)
    fare = db.Column(db.Float, default=-1)

    def __init__(self, passengerId, name, survived, sex, age, fare):
        self.passengerId = passengerId
        self.name = name
        self.survived = survived
        self.sex = sex
        self.age = age
        self.fare = fare

    def __repr__(self):
        return str(self.passengerId) + " - " + str(self.name) + " - " + str(self.age)


@app.cli.command("load-data")
@click.argument("fname")
def load_data(fname):
    print('Ładuje dane z pliku' + fname)
    df = pd.read_csv(fname)
    for row in df.itertuples(index=False):
        print('***********************')
        v_passenger_id = row[0]
        v_survived = row[1]
        v_name = row[3]
        v_sex = row[4]
        v_age = row[5]
        v_fare = row[9]
        print('PassengerId = ' + str(v_passenger_id))
        print('Survived = ' + str(v_survived))
        print('Name = ' + str(v_name))
        print('Sex = ' + str(v_sex))
        print('Age = ' + str(v_age))
        print('Fare = ' + str(v_fare))

        obj = Data(v_passenger_id, v_survived, v_name, v_sex, v_age, v_fare)
        db.session.add(obj)
    db.session.commit()


@app.route('/')
def hello():
    retVal = 'Witaj, baza posiada (' + str(len(Data.query.all())) + ') wierszy.'
    retVal += '<br/> Zobacz załadowane dane <a href="/data">TUTAJ</a>.'
    return retVal


@app.route('/data')
def data():
    retVal = 'Rows = ' + str(len(Data.query.all())) + '<br>'
    for row in Data.query.all():
        retVal += '<br>' + str(row.__repr__())
    return retVal
