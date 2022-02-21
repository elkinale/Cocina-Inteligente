# Configuración Rapsberry Pi como servidor


## Instalación de Apache

```bash
sudo apt update
sudo apt upgrade
sudo apt install apache2

# Revisar el estado de servicio de apache
systemctl status apache.service
```

Una vez realizado esto se puede verificar su correcta instalación con la IP de la Raspberry desde el navegador.  
Los archivos se encuentran en /var/www/html/index.html  

[Apache](https://ubuntu.com/server/docs/web-servers-apache#:~:text=Apache%20is%20the%20most%20commonly,pages%20requested%20by%20client%20computers.&text=This%20configuration%20is%20termed%20LAMP,deployment%20of%20Web%2Dbased%20applications.)

## Configuración wsgi

```bash
sudo apt install libapache2-mod-wsgi
```
Archivo run.wsgi

```python
activate_this = 'Path_venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, "Path_application")
from main import app as application
```
Configurar Apache

```bash
<VirtualHost *>
    ServerName example.com

    WSGIDaemonProcess yourapplication user=user1 group=group1 threads=5
    WSGIScriptAlias / /var/www/yourapplication/yourapplication.wsgi

    <Directory /var/www/yourapplication>
        WSGIProcessGroup yourapplication
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>
</VirtualHost>  
```



[wsgi](https://flask.palletsprojects.com/en/0.12.x/deploying/mod_wsgi/)

## Instalación Mariadb

```bash
sudo apt install mariadb-server
sudo apt-get install libmysqlclient15-dev
sudo mysql_secure_installation

# Revisar el estado de servicio de base de datos
systemctl status mariadb.service
```
[mariadb_install](https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-on-ubuntu-20-04)

## Creación de Entorno Virtual
El entorno virtual en Python es un entorno donde el interprete de python, librerias y scripts instalados dentro de este estan aislados de otros entornos virtuales y aisla las librerias instaladas del "sistema".   

[venv](https://docs.python.org/3/library/venv.html#:~:text=A%20virtual%20environment%20is%20a,part%20of%20your%20operating%20system.)   

```bash
python3 -m venv Path_directory/name_venv
```
Una vez se ejecuto el comando se crea una carpeta con el nombre que se le asigno. De ahora en adelante se recomienda usar el entorno virtual para todo lo relacionado con **Python**.

```bash
# Activar entorno virtual
source Path_directory/name_env/bin/activate
ó
. Path_directory/name_env/bin/activate

# Desactivar entorno virtual
deactivate
```

## Micro FrameWork Flask

Se debe crear las carpetas con los nombres **static** y **templates** en la carpeta de trabajo.  
La carpeta de **static** se usa para los archivos de css y javascript.  
La carpeta de **templates** se usa para los archivos html.  

[Flask](https://flask.palletsprojects.com/en/2.0.x/)
```bash
pip3 install Flask
```

## Archivo Principal

```python
from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```


## Integración Base de Datos en servidor web con ORM

```bash
pip3 install SQLAlchemy
```
En el archivo principial agregar.

```python
from flask_sqlalchemy import SQLAlchemy


# Use to encrypt data
app.config['SECRET_KEY']='xyz'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# At the end need the name of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/data_base_name'

#A class is created asociated to a databse, the variables are the columns of the table
class Recipes(db.Model):   
    
    __tablename__ = 'tables_name'
    # Colocar tipo de dato de la columna y otras caracteristicas
    column_name = db.Column(db.Integer, primary_key = True)
```

[sql_alchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/)


