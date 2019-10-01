# RpiStatus
Logs raspberry pi's stats like temperature, memory usage and more..

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
$ python3 src/main/StatusCheckerThread.py
```

## Additional dependencies
###### [pymongo](https://api.mongodb.com/python/current/)
###### [dnspython](https://pypi.org/project/dnspython/)