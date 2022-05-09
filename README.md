# RestFulService

This project was developed in python3.9 and thus we recommend using this version of python or higher. Similar versions would probably work as well.
We have compiled a list of dependencies in *requirements.txt*. 

To run this project navigate to the top-level-directory and use `python3 main.py`. Afterwards, the service will be running locally on address localhost:5000 and you can make the specified requests.

Register user: ```curl -d 'user=<user>&password=<password>' http://127.0.0.1:5001/users```

Login: ```curl -d 'user=<user>&password=<password>' http://127.0.0.1:5001/users/login```

Shorten URL ```curl -d 'url=https://google.com' http://127.0.0.1:5000```

Lookup shortened URLS ```curl -v http://127.0.0.1:5000```

Docker admin side build, enter the admin folder: ```docker build -t admin .```

Docker frontend side build, enter the frontend folder: ```docker build -t frontend .```

execute the flask apps inside the containers, again enter the corresponding folder:

```docker run -p 5001:5001 -t -i admin:latest```

```docker run -p 5000:5000 -t -i frontend:latest```

The IP addresses inside the containers change, so according to our code structure, first start the frontend docker container, then the admin.

Register: ```curl -d 'user=user&password=password' http://172.17.0.3:5000/users```

Login: ```curl -d 'user=user&password=password' http://172.17.0.3:5000/users/login```

shorten URL: ```curl -d 'url=https://google.com' http://172.17.0.2:5000/```

the frontend side IP will be ```http://172.17.0.2:5000/``` and the admin side ```http://172.17.0.3:5000/```

it is necessary to open the frontend side first.
