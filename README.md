# RestFulService

This project was developed in python3.9 and thus we recommend using this version of python or higher. Similar versions would probably work as well.
We have compiled a list of dependencies in *requirements.txt*. 

To run this project navigate to the top-level-directory and use `python3 main.py`. Afterwards, the service will be running locally on address localhost:5000 and you can make the specified requests.

Register user: ```curl -d 'user=<user>&password=<password>' http://127.0.0.1:5000/users```
Login: ```curl -d 'user=<user>&password=<password>' http://127.0.0.1:5000/users/login```
Shorten URL ```curl -d 'url=https://google.com' http://127.0.0.1:5000```
Lookup shortened URLS ```curl -v http://127.0.0.1:5000```
