from flask import Blueprint, jsonify, request
from .models import Tool, db  # Make sure db is imported here

main = Blueprint('main', __name__)

@main.route('/tools', methods=['GET'])
def get_tools():
    tools = Tool.query.all()
    return jsonify([tool.to_dict() for tool in tools])

@main.route('/tools', methods=['POST'])
def create_tool():
    data = request.get_json()
    new_tool = Tool(name=data['name'], description=data['description'])
    db.session.add(new_tool)
    db.session.commit()
    return jsonify(new_tool.to_dict()), 201

@main.route('/tools/<int:id>', methods=['PATCH'])
def update_tool(id):
    data = request.get_json()
    tool = Tool.query.get_or_404(id)
    tool.name = data.get('name', tool.name)
    tool.description = data.get('description', tool.description)
    db.session.commit()
    return jsonify(tool.to_dict())

@main.route('/tools/<int:id>', methods=['DELETE'])
def delete_tool(id):
    tool = Tool.query.get_or_404(id)
    db.session.delete(tool)
    db.session.commit()
    return '', 204
