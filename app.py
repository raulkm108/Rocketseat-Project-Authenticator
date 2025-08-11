from flask import Flask
from database import db
from models.user import User
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)


@app.route("/hello-world", methods=["GET"])
def hello_world ():
    return "Hello world"

if __name__ == '__main__':
    app.run(debug=True)
