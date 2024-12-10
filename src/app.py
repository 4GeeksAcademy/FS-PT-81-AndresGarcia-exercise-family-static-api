"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
Jackson_family = FamilyStructure("Jackson")

Jon = {
    "First name": "Jon",
    "Last name": Jackson_family.last_name,
    "age": 24,
    "lucky_numbers": [21,1,10]
}

Jane = {
    "First name": "Jane",
    "Last name": Jackson_family.last_name,
    "age": 24,
    "lucky_numbers": [31,1,25]
}

Jimmy = {
    "First name": "Jimmy",
    "Last name": Jackson_family.last_name,
    "age": 24,
    "lucky_numbers": [14,9,6]
}

Jackson_family.add_member(Jon)
Jackson_family.add_member(Jane)
Jackson_family.add_member(Jimmy)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_members():
    members = Jackson_family.get_all_members()
    return jsonify(members), 200



@app.route('/member/<int:id>', methods=['GET'])
def get_single_member(id):
    member = Jackson_family.get_member(id)
    return jsonify(member), 200



@app.route('/member', methods=['POST'])
def create_member():
    member = request.json
    print("added", member)
    Jackson_family.add_member(member)
    if member is not None:
        return "member created", 200   


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_single_member(id):
    member = Jackson_family.get_member(id)
 
    if member:
        Jackson_family.delete_member(id)
        return jsonify({"message": f"Member deleted successfully: {member}"}), 200
    else:
        return jsonify({"error": "Member not found"}), 404

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
