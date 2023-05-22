import mysql.connector
import click #herramienta para poder ejecutar comandos en cmd para conexion a bd
from flask import current_app, g #mantiene la aplicacion que estamos ejecutando y g: se le pueden asignar variables para despues accederlas desde otra parte de la aplicacion
from flask.cli import with_appcontext # contexto de la configuracion de la aplicacion, se pueden acceder a las variables de configuracion de la aplicacion como el host de la base de datos, su usuario y password
from flask import Flask
import os

'''Variable vital para la ejecucion y funcionamiento de flask'''
app = Flask(__name__)

instructions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'CREATE TABLE IF NOT EXISTS `user` ('
    '   `id` INT PRIMARY KEY AUTO_INCREMENT,'
    '   `username` VARCHAR(50) UNIQUE NOT NULL,'
    '   `password` VARCHAR(100) NOT NULL'
    ');',
    'CREATE TABLE IF NOT EXISTS `todo` ('
    '   `id` INT PRIMARY KEY AUTO_INCREMENT,'
    '   `created_by` INT NOT NULL,'
    '   `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,'
    '   `description` TEXT NOT NULL,'
    '   `completed` BOOLEAN NOT NULL,'
    '   FOREIGN KEY (`created_by`) REFERENCES `user`(`id`)'
    ');',
    'SET FOREIGN_KEY_CHECKS=1;'
]



'''Define el string de conexion por utilizar para la conexion a la base de datos'''
def get_db():
    if 'db' not in g:
        db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        c = db.cursor(dictionary=True)
    return db, c

'''Permite que el usuario introduzca las credenciales de la base de datos en la terminal por medio de os y flask'''
app.config.from_mapping(
    SECRET_KEY='mikey',  # Define las sesiones en nuestra aplicacion (cookie)
    DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
    DATABASE_PORT=os.environ.get('FLASK_DATABASE_PORT', 3306),
    DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
    DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
    DATABASE=os.environ.get('FLASK_DATABASE')
)

'''Ejecuta las instrucciones de cracion de las tablas en la base de datos'''
def init_db():
    db, c = get_db()
    for i in instructions:
        c.execute(i)
    db.commit()

@click.command('init-db') #este comando se podra utilizar en la terminal para ejecutar la base de datos
@with_appcontext #indica que utiliza el contexto de la aplicacion para que pueda acceder a las variables de DATABASE_HOST, DATABASE_USER, ETC
def init_db_command():
    init_db()
    click.echo('Base de datos inicializada')

'''Redirecciona a la pagina inicial de la aplicacion y ejecuta la consulta'''
@app.route('/')
def index():
    # Ejemplo de consulta a la base de datos
    db, c = get_db()
    c.execute(
        'select * from user'
    )
    result = c.fetchall()
    c.close()
    return str(result)

'''Inicializa la base de datos y la aplicacion con flask'''
if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)

