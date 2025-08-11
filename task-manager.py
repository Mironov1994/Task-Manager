from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

# Создание экземпляра приложения Flask
app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # База данных SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Секретный ключ для JWT
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)  # Время жизни токена

# Инициализация базы данных и JWT
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Модели данных для пользователей и задач

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True)

    # Метод для хеширования пароля
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Метод для проверки пароля
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    due_date = db.Column(db.String(50), nullable=True)
    priority = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Создание базы данных
@app.before_first_request
def create_tables():
    db.create_all()

# Регистрация пользователя
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Проверка, есть ли уже такой пользователь
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email is already registered'}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User successfully registered'}), 201

# Авторизация пользователя и получение токена
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Генерация токена
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token})

# Создание задачи (требуется аутентификация)
@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    current_user_id = get_jwt_identity()  # Получаем ID текущего пользователя
    data = request.get_json()

    title = data.get('title')
    description = data.get('description', '')
    due_date = data.get('due_date', '')
    priority = data.get('priority', 1)
    created_at = updated_at = str(datetime.now())

    # Создание новой задачи
    new_task = Task(
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
        created_at=created_at,
        updated_at=updated_at,
        user_id=current_user_id
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        'id': new_task.id,
        'title': new_task.title,
        'description': new_task.description,
        'due_date': new_task.due_date,
        'priority': new_task.priority,
        'created_at': new_task.created_at,
        'updated_at': new_task.updated_at
    }), 201

# Получение всех задач пользователя (требуется аутентификация)
@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=current_user_id).all()

    task_list = []
    for task in tasks:
        task_list.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date,
            'priority': task.priority,
            'created_at': task.created_at,
            'updated_at': task.updated_at
        })

    return jsonify(task_list)

# Получение конкретной задачи по ID (требуется аутентификация)
@app.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    current_user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

    if task is None:
        return jsonify({'message': 'Task not found'}), 404

    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date,
        'priority': task.priority,
        'created_at': task.created_at,
        'updated_at': task.updated_at
    })

# Обновление задачи (требуется аутентификация)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

    if task is None:
        return jsonify({'message': 'Task not found'}), 404

    data = request.get_json()

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.due_date = data.get('due_date', task.due_date)
    task.priority = data.get('priority', task.priority)
    task.updated_at = str(datetime.now())

    db.session.commit()

    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date,
        'priority': task.priority,
        'created_at': task.created_at,
        'updated_at': task.updated_at
    })

# Удаление задачи (требуется аутентификация)
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

    if task is None:
        return jsonify({'message': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return '', 204

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)