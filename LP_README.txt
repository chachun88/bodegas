# IMPORTANTE:

```sh
$ sudo pip install --upgrade -r requirements.txt
```

Para que funcione la carga masiva, se debe instalar xlrd
que es una librería para leer excell

página de xlrd : https://github.com/python-excel/xlrd
para instalar xlrd con pip

$ sudo pip install xlrd

*******************************************************

al configurar en una maquina definitiva, se debe aumentar el timeout para que funcione la carga masiva con excel


```sh
watchmedo shell-command \
    --patterns="*.py" \
    --command='clear && python -m test' \
    --recursive \
    /Users/ricardo/git_loadingplay/bodegas.git/
´´´


## coverage

```sh
coverage erase & coverage run -m test & coverage html -d coverage_html -i
```

# Execute on ondev

```sh
$ sudo su git2
$ python bodegas.py &
```
