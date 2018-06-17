# EduConv-Backend


### Init database
Following command will init empty db and insert mnist into datasets column 
You may need to have sqlite3 installed
```
python3 db_models.py
```

### Running app

```  
pip install -m requirements.txt
export FLASK_APP=./main.py
python3 -m flask run --host=HOST_IP --port=PORT
```
  default host is 127.0.0.1  
  default port is 5000
  
127.0.0.1 will work only on your computer. You can allow any connection from anywhere LAN using `--host=0.0.0.0`

### adding cifar10

```
cd datasets
python3
import sqlite3
from cifar10 import Cifar10Input
db = sqlite3.connect("../db.sqlite")
Cifar10Input.acquire(db)
db.close()
quit()
cd ..
```