# RpiStatus
Logs raspberry pi's stats like temperature, memory usage and more..

![Example data](https://imgur.com/Fq4jshY.png)

## Installation
##### 1. Clone or download project
##### 2. Install python 3.*
##### 3. Go to project directory
##### 4. Set python path here
```sh
$ export PYTHONPATH='.'
```
##### 5. Config app in `src/configs/config.py`
##### 6. Run app
```sh
$ python3 src/main/App.py
```

## Dependencies
###### [pymongo](https://api.mongodb.com/python/current/)
###### [dnspython](https://pypi.org/project/dnspython/)
###### [flask](https://github.com/pallets/flask)
###### [flask-restful](https://flask-restful.readthedocs.io/en/latest/)