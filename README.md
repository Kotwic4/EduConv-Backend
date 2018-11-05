# EduConv-Backend

### Init database
Following command will init empty db and insert datasets info.
You may need to have sqlite3 installed

#### Linux
```
python3 init_db.py
```

#### Windows
```
python init_db.py
```

### Running app

#### Linux

```  
pip install -m requirements.txt
export FLASK_APP=./main.py
python3 -m flask run --host=HOST_IP --port=PORT
```

#### Windows

```
pip install -r requirements.txt
set FLASK_APP=./main.py
python -m flask run --host=HOST_IP --port=PORT
```

default host is 127.0.0.1
default port is 5000

127.0.0.1 will work only on your computer. You can allow any connection from anywhere LAN using `--host=0.0.0.0`

### Running tests:
```
python3 -m unittest
```
You can also run all tests in specific module or even single test by simply passing it as an arg for unittest:
```
python3 -m unittest src.test.test_SchemaValidator.test_validate_dropout_layer_after_dropout_layer
```