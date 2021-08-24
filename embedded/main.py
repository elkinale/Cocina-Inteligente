from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import json

#Se crea la aplicación
app = Flask(__name__)
app.config['SECRET_KEY']='xyz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:paswd@localhost/classicmodels'

# #Se crea la base de datos
db = SQLAlchemy(app)

# #Variables son los elementos de la base de datos
class Reads(db.Model):

    __tablename__ = 'employees'
    employeeNumber = db.Column(db.Integer, primary_key=True)
    lastName = db.Column(db.String(50))
    firstName = db.Column(db.String(50))
    extension = db.Column(db.String(10))
    email = db.Column(db.String(100),)
    officeCode = db.Column(db.String(10))
    reportsTo = db.Column(db.Integer)
    jobTitle =db.Column(db.String(50))


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/stats/')
def stats():
    return render_template('stats.html')

@app.route('/lecturas/')
def get_lecturas():
    lecturas = Reads.query.all()
    response = []
    for lectura in lecturas:
        data = {
            'number' : lectura.employeeNumber,
            'last name' : lectura.lastName,
            'first name' : lectura.firstName,
            'extension' : lectura.extension,
            'email' : lectura.email,
            'office code' : lectura.officeCode,
            'report to' : lectura.reportsTo,
            'job title' : lectura.jobTitle
        }
        response.append(data)
    return json.dumps(response, ensure_ascii=False).encode('utf-8')

# @app.route('/lecturasById/<valor>')
# def get_lecturas_by_id(valor):
#     lecturas = Reads.query.filter_by(id=valor).all()
#     response = []
#     for lectura in lecturas:
#         data={
#             'id': lectura.id,
#             'topico': lectura.topico,
#             'payload': lectura.payload

#         }
#         response.append(data)

#         return json.dumps(response, ensure_ascii=False).encode('utf-8')

@app.route('/images/')
def images():
    return render_template('images.html')

@app.route('/recepies/', methods=['GET', 'POST'])
def recepies():
    return render_template('recepies.html')

if __name__ == '__main__':
    app.run(debug=True)
