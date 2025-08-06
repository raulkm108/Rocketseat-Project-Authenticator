from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

@app.route("", methods=["GET"])

if __name__ == '__name__':
    app.run(debug=True)