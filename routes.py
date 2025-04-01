from flask import Blueprint, jsonify, request, abort
from models import db, Tool, User
from auth import requires_auth, AuthError

api_bp = Blueprint('api', __name__)


# Define the root route
@api_bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Cybersecurity Tools Management API!"})


# GET a specific tool
@api_bp.route('/tools/<int:tool_id>', methods=['GET'])
@requires_auth('read:tools')
def get_tool(tool_id):
    tool = Tool.query.get(tool_id)
    if tool is None:
        abort(404)
    return jsonify({
        "success": True,
        "tool": tool.serialize()
    })


# POST a new tool
@api_bp.route('/tools', methods=['POST'])
@requires_auth('create:tools')
def create_tool():
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'description' not in data or 'user_id' not in data:
            abort(400)

        # Sanitize inputs
        name = data['name'].strip()
        description = data['description'].strip()
        user_id = data['user_id']

        # Check if user exists
        user = User.query.get(user_id)
        if user is None:
            abort(404, description="User not found")

        # Create and save the new tool
        new_tool = Tool(name=name, description=description, user_id=user_id)
        db.session.add(new_tool)
        db.session.commit()

        return jsonify({
            "success": True,
            "tool": new_tool.serialize()
        }), 201
    except KeyError:
        # If any of the required fields are missing, return 400 Bad Request
        abort(400)
    except Exception as e:
        db.session.rollback()  # Rollback any changes if an error occurs
        abort(422)


# GET all tools
@api_bp.route('/tools', methods=['GET'])
@requires_auth('read:tools')
def get_tools():
    tools_list = Tool.query.all()  # Fetch all tools from the database
    return jsonify({
        "success": True,
        "tools": [tool.serialize() for tool in tools_list]
    })


# PATCH an existing tool
@api_bp.route('/tools/<int:tool_id>', methods=['PATCH'])
@requires_auth('update:tools')
def update_tool(tool_id):
    tool = Tool.query.get(tool_id)
    if tool is None:
        abort(404)

    try:
        data = request.get_json()
        if not data:
            abort(400)

        if 'name' in data:
            tool.name = data['name']
        if 'description' in data:
            tool.description = data['description']

        db.session.commit()

        return jsonify({
            "success": True,
            "tool": tool.serialize()
        })
    except Exception:
        db.session.rollback()
        abort(422)


# DELETE a tool
@api_bp.route('/tools/<int:tool_id>', methods=['DELETE'])
@requires_auth('delete:tools')
def delete_tool(tool_id):
    tool = Tool.query.get(tool_id)
    if tool is None:
        abort(404)

    try:
        db.session.delete(tool)
        db.session.commit()

        return jsonify({
            "success": True,
            "deleted": tool_id
        })
    except Exception:
        db.session.rollback()
        abort(422)


# GET all users
@api_bp.route('/users', methods=['GET'])
@requires_auth('read:tools')
def get_users():
    users = User.query.all()
    return jsonify({
        "success": True,
        "users": [user.serialize() for user in users]
    })


# Error handler for AuthError
@api_bp.errorhandler(AuthError)
def handle_auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
