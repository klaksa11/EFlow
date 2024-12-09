from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///energyflow.db'  # Настраиваем базу данных SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Для безопасности сессий

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# Маршрут для регистрации
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():  # Устанавливаем контекст приложения
        db.create_all()  # Создаём таблицы в базе данных
    app.run(debug=True)
