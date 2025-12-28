import os

from flask import Flask

from models import db

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'data/db.sqlite')}"
)

db.init_app(app)

with app.app_context():
    db.create_all()



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press F9 to toggle the breakpoint.



if __name__ == '__main__':
    print_hi('PyCharm')

