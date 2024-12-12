from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cache.sqlite"
app.config["SECRET_KEY"] = "abcd123"
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# User model
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

# Initialize the database (this should be done once for setup)
with app.app_context():
    db.create_all()

# User loader for Flask-Login
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

# Routes
@app.route('/')
def loginPage():
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def registerPage():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process the login form data
        username = request.form.get("username")
        password = request.form.get("password")
        user = Users.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return jsonify({"message": "Login successful!"}), 200
        return jsonify({"error": "Invalid credentials!"}), 401
    # Render the login page when the method is GET
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get("username")
    if Users.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists!"}), 400
    user = Users(
        username=username,
        password=request.form.get("password"),
        # If you want to store additional fields like name and email:
        first_name=request.form.get("firstName"),
        last_name=request.form.get("lastName"),
        email=request.form.get("email"),
        phone_number=request.form.get("phoneNumber")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered!"}), 201


@app.route('/profile')
@login_required
def profile():
    return jsonify({"message": f"Welcome to your profile, {current_user.username}!"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
