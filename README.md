# covid19forecastSARIMA
A flask app that train a SARIMA model on covid19 cases in France and make prediction 

# install 

Best practice is to use a virtual env
```shell
virtualenv env
source ./env/bin/activate
````
Then install all packages included in requirements.txt
```shell
pip install -r requirements.txt
```

Finaly, you can run the app inside a WSGI container : 
```shell
python wsgi.py
```