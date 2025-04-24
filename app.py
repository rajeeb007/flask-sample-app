# app.py
from flask import Flask, jsonify, request, render_template
import os
from datetime import datetime

app = Flask(__name__)

# In-memory storage for notes
notes = [
    {"id": 1, "title": "Welcome Note", "content": "Welcome to this Flask application!", "created_at": datetime.now().isoformat()},
    {"id": 2, "title": "Flask Info", "content": "Flask is a lightweight web framework for Python.", "created_at": datetime.now().isoformat()}
]

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html', server_time=datetime.now())

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/info')
def info():
    """Return information about the server."""
    return jsonify({
        "app_name": "Flask Demo App",
        "environment": os.environ.get("FLASK_ENV", "development"),
        "python_version": os.environ.get("PYTHON_VERSION", "3.9"),
        "timestamp": datetime.now().isoformat()
    })

# Notes API endpoints
@app.route('/api/notes', methods=['GET'])
def get_notes():
    """Get all notes."""
    return jsonify({"notes": notes})

@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID."""
    note = next((note for note in notes if note["id"] == note_id), None)
    if note:
        return jsonify({"note": note})
    return jsonify({"error": "Note not found"}), 404

@app.route('/api/notes', methods=['POST'])
def create_note():
    """Create a new note."""
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({"error": "Title and content are required"}), 400
    
    new_note = {
        "id": len(notes) + 1,
        "title": data['title'],
        "content": data['content'],
        "created_at": datetime.now().isoformat()
    }
    
    notes.append(new_note)
    return jsonify({"note": new_note}), 201

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update an existing note."""
    note = next((note for note in notes if note["id"] == note_id), None)
    if not note:
        return jsonify({"error": "Note not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if 'title' in data:
        note['title'] = data['title']
    if 'content' in data:
        note['content'] = data['content']
    
    return jsonify({"note": note})

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a note."""
    global notes
    note = next((note for note in notes if note["id"] == note_id), None)
    if not note:
        return jsonify({"error": "Note not found"}), 404
    
    notes = [note for note in notes if note["id"] != note_id]
    return jsonify({"message": f"Note {note_id} deleted successfully"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)