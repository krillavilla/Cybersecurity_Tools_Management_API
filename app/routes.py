from flask import request, jsonify
from . import app, db
from .models import Tool
from .auth import requires_auth


@app.route('/tools', methods=['GET'])
@requires_auth('view:tools')
def get_tools():
    tools = Tool.query.all()
    return jsonify([tool.serialize() for tool in tools])


@app.route('/tools', methods=['POST'])
@requires_auth('create:tool')
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
