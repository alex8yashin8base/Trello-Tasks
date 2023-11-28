from flask import Flask, jsonify, request, make_response
import json
import os
from typing import Dict, Any

app = Flask(__name__)
data_file = 'data.txt'

def read_data() -> Dict[str, Any]:
    if not os.path.exists(data_file):
        return {}
    with open(data_file, 'r') as file:
        return json.load(file)

def write_data(data: Dict[str, Any]) -> None:
    with open(data_file, 'w') as file:
        json.dump(data, file)

@app.route('/notes', methods=['GET'])
def get_notes() -> Any:
    data = read_data()
    return make_response(jsonify(data), 200)

@app.route('/notes/<key>', methods=['GET'])
def get_note(key: str) -> Any:
    data = read_data()
    note = data.get(key)
    if note:
        return jsonify({key: note})
    return make_response(jsonify({"error": "Note not found"}), 404)

@app.route('/notes', methods=['POST'])
def add_note() -> Any:
    data = read_data()
    note_data = request.json
    for key, value in note_data.items():
        data[key] = value
    write_data(data)
    return make_response(jsonify({"message": "Data updated"}), 200)

@app.route('/notes/<key>', methods=['DELETE'])
def delete_note(key: str) -> Any:
    data = read_data()
    if key not in data:
        return make_response(jsonify({"error": "Note not found"}), 404)
    data.pop(key)
    write_data(data)
    return make_response(jsonify({"message": "Note deleted"}), 200)

@app.route('/notes', methods=['DELETE'])
def delete_all_notes() -> Any:
    write_data({})
    return make_response(jsonify({"message": "All notes deleted"}), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0')