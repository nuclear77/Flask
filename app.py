from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# Настройка базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

# Настройка миграции
migrate = Migrate(app, db)

# Определение модели данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, username):
        self.username = username

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('user_list'))
    return render_template('create_user.html')

@app.route('/users')
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return jsonify({"id": user.id, "username": user.username})
    else:
        return jsonify({"message": "User not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
