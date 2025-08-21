from flask import Flask, request, jsonify
from database import db
from models.user import User
from flask_login import LoginManager, login_user, current_user, logout_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/login", methods=["POST"])
def login ():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
    
        user = User.query.filter_by(username=username).first()
         
        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "You have successfully logged in"})

    return jsonify({"message": "Invalid Credentials"}), 400

@app.route('/logout', methods=['GET'])
@login_required

def logout():
    logout_user()
    return jsonify({"message":"You have successfully logged out" })

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User successfully registered"})


    return jsonify({"message": "Invalid data"}), 400

@app.route('/user/<int:id_user>', methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return {"username:": user.username}

    return jsonify({"message": "User not found!"}), 404

@app.route('/user/<int:id_user>', methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if user and data.get("password"):
        user.pasword = data.get("password")
        db.session.commit()

        return jsonify ({"message": f"User {id_user} was successfully updated!"})
    
    return jsonify({"message": "User not found!"}), 404 

@app.route('/user/<int:id_user>', methods=["DELETE"])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if id_user == current_user.id:
        return jsonify ({"message": "You are not allowed to delete this user"}), 403


    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify ({"message": f"User {id_user} was successfuly deleted"})
    
    return jsonify ({"message": "User not found!"}), 404

if __name__ == '__main__':
    app.run(debug=True)
