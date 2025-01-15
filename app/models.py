from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    platform = db.Column(db.String(50))
    license = db.Column(db.String(50))

    def __repr__(self):
        return f'<Tool {self.name}>'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'platform': self.platform,
            'license': self.license,
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
        }