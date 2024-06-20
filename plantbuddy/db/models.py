from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from flask_login import UserMixin

class Customer(db.Model, UserMixin):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    plants = db.relationship("CustomerPlant", back_populates="customer")
    blog_posts = db.relationship("BlogPost", back_populates="author")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Customer %r>' % self.username

class Plant(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    photo = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    light = db.Column(db.String(50), nullable=True)  # Updated from placement
    humidity = db.Column(db.String(50), nullable=True)  # Updated from water_demand
    fertilizing = db.Column(db.String(50), nullable=True)  # weekly, monthly, -
    toxicity = db.Column(db.String(200), nullable=True)
    watering_frequency = db.Column(db.String(10), nullable=True)  # 1x, 2x, 5x

    customer_plants = db.relationship("CustomerPlant", back_populates="plant")
    care_tasks = db.relationship('CareTask', back_populates='plant')

    def __repr__(self):
        return f'<Plant {self.name}>'

class CustomerPlant(db.Model):
    __tablename__ = 'customer_plants'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    last_watered_date = db.Column(db.DateTime, nullable=True)

    customer = db.relationship("Customer", back_populates="plants")
    plant = db.relationship("Plant", back_populates="customer_plants")

    def __repr__(self):
        return f'<CustomerPlant customer_id={self.customer_id}, plant_id={self.plant_id}>'

class CareTask(db.Model):
    __tablename__ = 'care_tasks'
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    task_type = db.Column(db.String(50), nullable=False)  # 'Water' or 'Fertilize'
    task_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_completed = db.Column(db.Boolean, default=False)
    amount = db.Column(db.Float, nullable=False)

    plant = db.relationship('Plant', back_populates='care_tasks')

    def __repr__(self):
        return f'<CareTask {self.task_type} for {self.plant.name}>'

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    approved = db.Column(db.Boolean, default=False)

    author = db.relationship("Customer", back_populates="blog_posts")

    def __repr__(self):
        return f'<BlogPost {self.title} by {self.author.username}>'
