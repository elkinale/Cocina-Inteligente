from flask import Flask, render_template, url_for, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
#import detection_server
import time
import cv2

from sqlalchemy.sql.expression import asc

# The app is created
app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='xyz'
# At the end need the name of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:paswd@localhost/embedded'

# Capture video
PROTOCOL = 'http'
IP = '190.158.0.169'
EXTRA = 'cam-hi.jpg'

# The data base is created
db = SQLAlchemy(app)

#A class is created asociated to a databse, the variables are the columns of the table
class Recipes(db.Model):   
    
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(40), nullable=False)
    producto = db.Column(db.String(20), nullable=False)
    tipoPlato = db.Column(db.String(20), nullable=False)
    categoria = db.Column(db.String(20), nullable=False)
    tipoCoccion = db.Column(db.String(20))
    ingredientes = db.Column(db.Text)
    personas =db.Column(db.Integer)
    link = db.Column(db.String(150))  
    
class Measure(db.Model):
    
    __tablename__ = 'measures'
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    device = db.Column(db.String(30), nullable=False)   
    postDate = db.Column(db.DateTime, nullable=True)

def  gen_frames(frame=None):
    while True:
        camera = cv2.VideoCapture(f'{PROTOCOL}://{IP}/{EXTRA}')
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            #if not frame:
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            # else:
            #     return buffer
        
            
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame') 
        

@app.route('/')
def home():
    return render_template('home.html')
 
        
@app.route('/stats/', methods=['GET', 'POST'])
def stats():
        
    if request.method == 'POST':
        init_t = request.form['init_time']
        finish_t = request.form['finish_time']
        init_d = f"{request.form['init_date']} {init_t}"
        finish_d = f"{request.form['finish_date']} {finish_t}"
        
    else:
        init = datetime.now() - timedelta(hours=1)
        init_t = init.strftime('%H:%M')
        finish_t = datetime.now().strftime ('%H:%M')
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
                           time=time, temperature=temperature, humidity=humidity, 
                           init_t = init_t, finish_t =finish_t)


@app.route('/images/')
def images():
    camera = cv2.VideoCapture(f'{PROTOCOL}://{IP}/{EXTRA}')
    if camera.isOpened():
        ret, frame =camera.read()
        #detection_server.img = frame
        #time.sleep(2)
        #labels = detection_server.data
    else:
        labels = ()
    return render_template('images.html',labels=labels)

@app.route('/recipes/', methods=['GET', 'POST'])
def recipes():
   
    table = ()
    
    data = Recipes.query.all() 

    items1, items2 = set(' '), set(' ')
    for item in data:
            items1.add(item.tipoPlato)
            items2.add(item.producto)  
    
    items1, items2 = list(items1), list(items2)
    items1.sort(), items2.sort()        
           
    if request.method=='POST':
        
        item_1 = request.form['item_1']
        item_2 = request.form['item_2']     
        
        if not  item_1:
            data = Recipes.query.filter_by(producto=item_2).all()
        elif not item_2:
            data = Recipes.query.filter_by(tipoPlato=item_1).all()
        else:
            data = Recipes.query.filter_by(tipoPlato=item_1).filter_by(producto=item_2).all()
            
        labels = ['Nombre', 'Producto', 'Tipo de Plato', 'Categoria', 'Tipo de Cocción', 
                  'Ingredientes', 'Personas']
        table = []
        table.append(labels)    
        for row in data:   
            table.append([row.nombre, row.producto, row.tipoPlato, 
                                    row.categoria, row.tipoCoccion, row.ingredientes, 
                                    row.personas, row.link])
                      
    return render_template('recepies.html', items1=items1, items2=items2,table=table)

if __name__ == '__main__':
    app.run(debug=True)
