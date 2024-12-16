from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# Конфигурация приложения
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///energyflow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'

# Инициализация базы данных и bcrypt
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    height = db.Column(db.Float, nullable=True)  # Рост
    weight = db.Column(db.Float, nullable=True)  # Вес
    gender = db.Column(db.String(10), nullable=True)  # Пол
    is_admin = db.Column(db.Boolean, default=False)

# Создание таблиц (выполнять один раз)
with app.app_context():
    db.create_all()


# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        
        # Проверка уникальности email
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Пользователь с таким email уже существует. Попробуйте другой email.", "danger")
            return redirect(url_for('register'))
        
        # Добавление нового пользователя
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        try:
            db.session.commit()
            flash("Регистрация прошла успешно! Теперь войдите в систему.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash("Произошла ошибка при сохранении данных.", "danger")
            print(f"Ошибка: {e}")
            return redirect(url_for('register'))
    
    # Отображение формы регистрации
    return render_template('index.html')


# Вход в систему
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            session['is_admin'] = user.is_admin  # Сохраняем статус администратора

            if user.is_admin:
                flash('Добро пожаловать, Администратор!', 'success')
                return redirect(url_for('admin'))  # Сразу в админку
            else:
                flash('Добро пожаловать!', 'success')
                return redirect(url_for('profile'))
        else:
            flash('Неверный email или пароль.', 'danger')

    return render_template('login.html')



# Профиль пользователя
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Сначала войдите в систему.', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('Пользователь не найден.', 'danger')
        return redirect(url_for('login'))
    
    return render_template(
        'profile.html',
        username=user.username,
        email=user.email,
        height=user.height,
        weight=user.weight,
        gender=user.gender
    )

#обновления данных
@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        flash('Сначала войдите в систему.', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if user:
        user.height = request.form['height']
        user.weight = request.form['weight']
        user.gender = request.form['gender']
        db.session.commit()
        flash('Данные профиля обновлены!', 'success')
    else:
        flash('Пользователь не найден.', 'danger')
    
    return redirect(url_for('profile'))


# Выход из системы
@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('login'))

#АДМИН
@app.route('/admin', methods=['GET'])
def admin():
    query = User.query

    # Получение параметров из запроса
    name = request.args.get('name')
    email = request.args.get('email')
    gender = request.args.get('gender')
    min_height = request.args.get('min_height', type=float)
    max_height = request.args.get('max_height', type=float)
    min_weight = request.args.get('min_weight', type=float)
    max_weight = request.args.get('max_weight', type=float)

    # Фильтрация
    if name:
        query = query.filter(User.username.ilike(f"%{name}%"))
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    if gender:
        query = query.filter_by(gender=gender)
    if min_height:
        query = query.filter(User.height >= min_height)
    if max_height:
        query = query.filter(User.height <= max_height)
    if min_weight:
        query = query.filter(User.weight >= min_weight)
    if max_weight:
        query = query.filter(User.weight <= max_weight)

    users = query.all()
    return render_template('admin.html', users=users)



if __name__ == '__main__':
    app.run(debug=True)