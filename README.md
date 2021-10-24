# Criminalistas_Back_End
Repositorio backend para ingeniería del software

# Instalación y creación base de datos

## Creación entorno virtual

Antes de arrancar debemos crear un **entorno virtual**, para instalar todos los *packages* que se utilizarán en este proyecto. 

```
$ mkdir <directorio>
$ cd <directorio>
$ source bin/activate
```

## Instalación packages

Una vez en el entorno deben instalar los *packages* necesarios (fastapi, ponyorm, pymysql)

```
$ pip install fastapi
$ pip install "uvicorn[standard]"
$ pip install pony 
$ python3 -m pip install PyMySQL
$ pip install black
```

## Instalación SQLite 3

Después de realizar eso, lo segundo que deben hacer es crear la base de datos en *sqlite 3*.

```
$ sudo apt-get update
$ sudo apt-get install sqlite3
$ sqlite3 --version
$ sudo apt-get install sqlitebrowser
```

## Levantar fastapi

Una vez realizado todo, pueden levantar el servidor de fastapi de esta manera

```
$ uvicorn app:app --reload
```
y una vez levantado ingresan a: 

http://127.0.0.1:8000/docs 

o a 

http://127.0.0.1:8000/redoc
