from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    water_need = db.Column(db.String(50), nullable=True)
    fertilizer_need = db.Column(db.String(50), nullable=True)
    common_issues = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Plant {self.name}>'

class CareTask(db.Model):
    __tablename__ = 'caretask'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)
    task_type = db.Column(db.String(50), nullable=False)  # 'Water' or 'Fertilize'
    task_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_completed = db.Column(db.Boolean, default=False)

    plant = db.relationship('Plant', backref=db.backref('care_tasks', lazy=True))

    def __repr__(self):
        return f'<CareTask {self.task_type} for {self.plant.name}>'
