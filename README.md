# EduConv-Backend

### Install dependencies

Install dependencies required by app.

```
pip3 install -m requirements.txt
```

### Init database
Following command will init empty db and insert datasets info.

```
python3 init_db.py
```

### Running app

```  
pip3 install -m requirements.txt
export FLASK_APP=./main.py
python3 -m flask run --host=HOST_IP --port=PORT
```


default host is 127.0.0.1
default port is 5000

127.0.0.1 will work only on your computer. You can allow any connection from anywhere LAN using `--host=0.0.0.0`

### Running linter
Running linter which check code style.

```
pycodestyle .
```