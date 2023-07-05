# docker-mysql-python
Este repositorio contiene el código correspondiente a la creación de dos contenedores de Docker: uno con la base de datos MySQL y otro para correr la resolución del ejercicio en Python.

### ¿Cómo ejecutar la solución?
1. Una vez clonado localmente el proyecto, debemos posicionarnos en la carpeta **/src** desde la consola.
2. Luego, debemos ejecutar el comando: `docker-compose up`.
3. Al pasar unos segundos, se crearán los contenedores correspondientes con la denominación **python_app** y **mysql_db** (cabe destacar que si quería ponerle localhost al contenedor con la base de datos MySQL, luego al correr el python no me lo reconocía y tiraba error de conexión). Debemos crear la tabla **users** con los datos correspondientes. Para ello, realizamos:
  3.1. Nos conectamos al contenedor del MySQL vía Docker Desktop y vamos a la pestaña **Terminal** para ejecutar:  `mysql -u PSH -p ` y se nos pedirá la contraseña correspondiente al usuario.
  3.2. Paso siguiente, debemos correr las sentencias SQL que se encuentran el archivo **/src/mysql/init.sql**
4. Por último, debemos conectarnos al contenedor del Python y vamos a la pestaña **Terminal**. Una vez allí, corremos `python execution.py`. Cabe destacar que todos los pasos se loggean en un archivo de log almacenado en el path **/src/python/log/**
