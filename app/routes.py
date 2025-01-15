from flask import Flask, request, jsonify
from . import app, db
from .models import Tool
from .auth import requires_auth


@app.route('/tools', methods=['GET'])
@requires_auth('read:tools')
def get_tools():
    tools = Tool.query.all()
    return jsonify([tool.serialize() for tool in tools])


@app.route('/tools/<int:tool_id>', methods=['GET'])
@requires_auth('read:tools')
def get_tool(tool_id):
    tool = Tool.query.get_or_404(tool_id)
    return jsonify(tool.serialize())


@app.route('/tools', methods=['POST'])
@requires_auth('create:tools')
def create_tool():
    data = request.get_json()
    new_tool = Tool(
        name=data['name'],
        category=data['category'],
        platform=data['platform'],
        license=data['license']
    )
    db.session.add(new_tool)
    db.session.commit()
    return jsonify(new_tool.serialize()), 201


@app.route('/tools/<int:tool_id>', methods=['PATCH'])
@requires_auth('update:tools')
def update_tool(tool_id):
    tool = Tool.query.get_or_404(tool_id)
    data = request.get_json()
    if 'name' in data:
        tool.name = data['name']
    if 'category' in data:
        tool.category = data['category']
    if 'platform' in data:
        tool.platform = data['platform']
    if 'license' in data:
        tool.license = data['license']
    db.session.commit()
    return jsonify(tool.serialize())


@app.route('/tools/<int:tool_id>', methods=['DELETE'])
@requires_auth('delete:tools')
def delete_tool(tool_id):
    tool = Tool.query.get_or_404(tool_id)
    db.session.delete(tool)
    db.session.commit()
    return jsonify({"message": "Tool deleted"}), 200


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request"}), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found"}), 404
