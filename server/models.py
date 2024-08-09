from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name cannot be empty")
        elif Author.query.with_entities(Author.name).filter_by(name=name).first():
            raise ValueError("Name must be unique")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError("Invalid phone number length")
        elif re.search(r'\D', phone_number):
            raise ValueError("Phone number contains invalid characters")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title cannot be empty")
        if not re.search(r'\b(?:won\'t believe|secret|top|guess)\b', title.lower()):
            raise ValueError("Title must contain clickbait keywords")
        return title
    
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters")
        
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary must be less than 250 characters")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category != "Fiction" and category != "Non-Fiction":
            raise ValueError("Category must be either Fiction or Non-Fiction")


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
