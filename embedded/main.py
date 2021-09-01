from typing_extensions import Protocol
from flask import Flask, render_template, url_for, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import cv2

from sqlalchemy.sql.expression import asc

# The app is created
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='xyz'
# At the end need the name of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:paswd@localhost/classicmodels'

# Capture video
_protocol = 'http'
_ip = ''
_port = '81'
_extra = 'stream'
camera = cv2.VideoCapture(f'{_protocol}://{_ip}:{_port}/{_extra}')
# The data base is created
db = SQLAlchemy(app)

#A class is created asociated to a databseS, the variables are the columns of the table
class Recipes(db.Model):   
# The name of the table is placed
    __tablename__ = 'employees'
    employeeNumber = db.Column(db.Integer, primary_key=True)
    lastName = db.Column(db.String(50))
    firstName = db.Column(db.String(50))
    extension = db.Column(db.String(10))
    email = db.Column(db.String(100),)
    officeCode = db.Column(db.String(10))
    reportsTo = db.Column(db.Integer)
    jobTitle =db.Column(db.String(50))  
    
class Measure(db.Model):
    
    __tablename__ = 'measures'
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    postDate = db.Column(db.DateTime)
    device = db.Column(db.String(30))   

def  gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame') 
        

@app.route('/')
def home():
    return render_template('home.html')
 
        
@app.route('/stats/', methods=['GET', 'POST'])
def stats():
        
    if request.method == 'POST':
        init = request.form['init_time']
        finish = request.form['finish_time']
        init_d = f"{request.form['init_date']} {init}:00"
        finish_d = f"{request.form['finish_date']} {finish}:00"
        
    else:
        init_d = datetime.now() - timedelta(hours=1)
        init_d = init_d.strftime('%Y-%m-%d %H:%M:%S')
        finish_d = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

              
    data = Measure.query.all()                
    measures = Measure.query.filter(
            Measure.postDate > init_d).filter(
            Measure.postDate < finish_d).order_by(
            Measure.postDate.asc()).all()     
                        
    temperature = []
    humidity = []
    time = []
      
    dates = set()
    for date in data:
        dates.add(str(date.postDate)[:10])
        
    dates = list(dates)
    dates.sort()
         
    for measure in measures:
        temperature.append(measure.temperature)
        humidity.append(measure.humidity)
        time.append(str(measure.postDate)[-8:-2])             
    
    return render_template('stats.html', init_d=str(init_d)[:10], finish_d=str(finish_d)[:10], dates=dates, 
                           time=time, temperature=temperature, humidity=humidity)


@app.route('/images/')
def images():
    return render_template('images.html')

@app.route('/recipes/', methods=['GET', 'POST'])
def recipes():
   
    item_1 = ''
    item_2 = ''
    table = ()
    
    data = Recipes.query.all() 

    items1, items2 = set(), set()
    for item in data:
            items1.add(item.jobTitle)
            items2.add(item.officeCode)  
    
    items1, items2 = list(items1), list(items2)
    items1.sort(), items2.sort()        

    item_1, item_2 = '', ''
    
    cat_1 = 'Job Title'
    cat_2 = 'Office Code'
       
    if request.method=='POST':
        
        item_1 = request.form['item_1']
        item_2 = request.form['item_2']     
        
        data = Recipes.query.filter_by(jobTitle=item_1).filter_by(officeCode=item_2).all()
        labels = ['Employee Number', 'Last Name', 'First Name', 'Extension', 'Email', 'Office Code', 
                  'Reports To', 'Job Title']
        table = []
        table.append(labels)      
        for row in data:   
            table.append([row.employeeNumber, row.lastName, row.firstName, 
                                    row.extension, row.email, row.officeCode, 
                                    row.reportsTo, row.jobTitle])
                    
    return render_template('recepies.html', items1=items1, items2=items2, cat_1=cat_1, cat_2=cat_2, 
                           item_1=item_1, item_2=item_2, table=table)
 
if __name__ == '__main__':
    app.run(debug=True)
