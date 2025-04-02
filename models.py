from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Tool(db.Model):
    __tablename__ = 'tool'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tools', lazy=True))

    def __repr__(self):
        return f'<Tool {self.name}>'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_id': self.user_id
        }

    @classmethod
    def create_tool(cls, name, description, user_id):
        """
        Helper method to create a new tool in the database.

        Args:
            name (str): Name of the tool
            description (str): Description of the tool
            user_id (int): ID of the user who owns the tool

        Returns:
            Tool: The newly created tool
        """
        # Create the new tool
        new_tool = cls(
            name=name,
            description=description,
            user_id=user_id
        )

        # Save it to the database
        db.session.add(new_tool)
        db.session.commit()

        return new_tool

    @classmethod
    def get_tool(cls, tool_id):
        """
        Helper method to get a tool by ID.

        Args:
            tool_id (int): ID of the tool to retrieve

        Returns:
            Tool: The tool with the given ID, or None if not found
        """
        return cls.query.get(tool_id)

    @classmethod
    def get_all_tools(cls):
        """
        Helper method to get all tools.

        Returns:
            list: A list of all tools
        """
        return cls.query.all()

    def update(self, data):
        """
        Helper method to update a tool.

        Args:
            data (dict): Dictionary containing the fields to update

        Returns:
            Tool: The updated tool
        """
        if 'name' in data:
            self.name = data['name']
        if 'description' in data:
            self.description = data['description']

        db.session.commit()
        return self

    def delete(self):
        """
        Helper method to delete a tool.

        Returns:
            int: The ID of the deleted tool
        """
        tool_id = self.id
        db.session.delete(self)
        db.session.commit()
        return tool_id


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

    @classmethod
    def get_user(cls, user_id):
        """
        Helper method to get a user by ID.

        Args:
            user_id (int): ID of the user to retrieve

        Returns:
            User: The user with the given ID, or None if not found
        """
        return cls.query.get(user_id)

    @classmethod
    def get_all_users(cls):
        """
        Helper method to get all users.

        Returns:
            list: A list of all users
        """
        return cls.query.all()
