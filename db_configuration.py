from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    location = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    plants = relationship("CustomerPlant", back_populates="customer")
    blog_posts = relationship("BlogPost", back_populates="author")

class Plant(Base):
    __tablename__ = 'plants'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    disease_info = Column(Text, nullable=True)
    sunlight_needs = Column(String, nullable=False)
    humidity_needs = Column(String, nullable=False)
    watering_frequency = Column(String, nullable=False)

    customer_plants = relationship("CustomerPlant", back_populates="plant")

class CustomerPlant(Base):
    __tablename__ = 'customer_plants'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    plant_id = Column(Integer, ForeignKey('plants.id'), nullable=False)
    location = Column(String, nullable=False)

    customer = relationship("Customer", back_populates="plants")
    plant = relationship("Plant", back_populates="customer_plants")

class BlogPost(Base):
    __tablename__ = 'blog_posts'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    approved = Column(Boolean, default=False)

    author = relationship("Customer", back_populates="blog_posts")

# Engine und Session erstellen
engine = create_engine('sqlite:///plantbuddy.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
