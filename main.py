import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from core import app, routes

if __name__ == '__main__':
    app.run(port=5001, debug=True)