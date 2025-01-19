from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Tool
from models import Tool, User
from auth import requires_auth
from flask import Blueprint, jsonify, request

api_bp = Blueprint('api', __name__)


# Define the root route
@api_bp.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to the Cybersecurity Tools Management API!"
    }), 200

# GET a specific tool
@api_bp.route('/tools/<int:tool_id>', methods=['GET'])
@jwt_required()
def get_tool(tool_id):
    tool = Tool.query.get(tool_id)
    if tool:
        return jsonify(tool.serialize())
    return jsonify({"msg": "Tool not found"}), 404


# POST a new tool
@api_bp.route('/tools', methods=['POST'])
@jwt_required()
@requires_auth('create:tool')
def create_tool():
    data = request.get_json()
    if not data or not 'name' in data or not 'description' in data:
        return jsonify({"error": "Invalid input"}), 400

    # Sanitize inputs
    name = data['name'].strip()
    description = data['description'].strip()

    # Create and save the new tool
    new_tool = Tool(name=name, description=description, user_id=current_user.id)
    db.session.add(new_tool)
    db.session.commit()

    return jsonify(new_tool.serialize()), 201


# GET all tools
@requires_auth('read:tools')
@api_bp.route('/tools', methods=['GET'])
@jwt_required()
def get_tools():
    tools = Tool.query.all()
    return jsonify([tool.serialize() for tool in tools])





# PATCH an existing tool
@api_bp.route('/tools/<int:tool_id>', methods=['PATCH'])
@jwt_required()
@requires_auth('update:tool')
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
@jwt_required()
@requires_auth('delete:tool')
def delete_tool(tool_id):
    tool = Tool.query.get(tool_id)
    if not tool:
        return jsonify({"msg": "Tool not found"}), 404
    db.session.delete(tool)
    db.session.commit()
    return jsonify({"msg": "Tool deleted"}), 200


# GET all users
@api_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])


# Add a Dummy Favicon Route
@api_bp.route('/favicon.ico')
def favicon():
    return "", 204