from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Tool, User
from auth import requires_auth

api_bp = Blueprint('api', __name__)


# Define the root route
@api_bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Cybersecurity Tools Management API!"})


# GET a specific tool
@api_bp.route('/tools/<int:tool_id>', methods=['GET'])
@jwt_required()  # Ensure the request is authorized using JWT
def get_tool(tool_id):
    tool = Tool.query.get(tool_id)
    if tool:
        return jsonify(tool.serialize())
    return jsonify({"msg": "Tool not found"}), 404


# POST a new tool
@api_bp.route('/tools', methods=['POST'])
@jwt_required()  # Ensure the request is authorized using JWT
@requires_auth('create:tool')  # Ensure the user has the necessary permissions
def create_tool():
    try:
        data = request.get_json()
        if not data or not 'name' in data or not 'description' in data:
            return jsonify({"error": "Invalid input"}), 400

        # Sanitize inputs
        name = data['name'].strip()
        description = data['description'].strip()

        # Get the user ID from the JWT token
        user_id = get_jwt_identity()

        # Create and save the new tool
        new_tool = Tool(name=name, description=description, user_id=user_id)
        db.session.add(new_tool)
        db.session.commit()

        return jsonify(new_tool.serialize()), 201
    except Exception as e:
        db.session.rollback()  # Rollback any changes if an error occurs
        return jsonify({"error": str(e)}), 500


# GET all tools
@api_bp.route('/tools', methods=['GET'])
@jwt_required()  # Ensure the request is authorized using JWT
@requires_auth('read:tools')  # Ensure the user has the necessary permissions
def get_tools():
    tools_list = Tool.query.all()  # Fetch all tools from the database
    return jsonify({"tools": [tool.serialize() for tool in tools_list]})


# PATCH an existing tool
@api_bp.route('/tools/<int:tool_id>', methods=['PATCH'])
@jwt_required()  # Ensure the request is authorized using JWT
@requires_auth('update:tool')  # Ensure the user has the necessary permissions
def update_tool(tool_id):
    tool = Tool.query.get(tool_id)
    if not tool:
        return jsonify({"msg": "Tool not found"}), 404
    data = request.get_json()
    tool.name = data.get('name', tool.name)
    tool.description = data.get('description', tool.description)
    db.session.commit()
    return jsonify(tool.serialize())


# DELETE a tool
@api_bp.route('/tools/<int:tool_id>', methods=['DELETE'])
@jwt_required()  # Ensure the request is authorized using JWT
@requires_auth('delete:tool')  # Ensure the user has the necessary permissions
def delete_tool(tool_id):
    tool = Tool.query.get(tool_id)
    if not tool:
        return jsonify({"msg": "Tool not found"}), 404
    db.session.delete(tool)
    db.session.commit()
    return jsonify({"msg": "Tool deleted"}), 200


# GET all users
@api_bp.route('/users', methods=['GET'])
@jwt_required()  # Ensure the request is authorized using JWT
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])


# Protected route
@api_bp.route('/secure-route', methods=['GET'])
@jwt_required()  # Ensure the request is authorized using JWT
def secure_route():
    return jsonify({"message": "Secure content"})
