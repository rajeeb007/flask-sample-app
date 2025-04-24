// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    fetchNotes();
    
    // Form submission
    document.getElementById('note-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const title = document.getElementById('title').value;
        const content = document.getElementById('content').value;
        
        createNote(title, content);
    });
});

// Fetch all notes
function fetchNotes() {
    fetch('/api/notes')
        .then(response => response.json())
        .then(data => {
            displayNotes(data.notes);
        })
        .catch(error => console.error('Error fetching notes:', error));
}

// Display notes in the UI
function displayNotes(notes) {
    const notesList = document.getElementById('notes-list');
    notesList.innerHTML = '';
    
    if (notes.length === 0) {
        notesList.innerHTML = '<li>No notes found. Create one!</li>';
        return;
    }
    
    notes.forEach(note => {
        const noteItem = document.createElement('li');
        noteItem.className = 'note-item';
        noteItem.innerHTML = `
            <div class="note-title">${note.title}</div>
            <div class="note-content">${note.content}</div>
            <div class="note-meta">Created: ${new Date(note.created_at).toLocaleString()}</div>
            <button class="delete-btn" data-id="${note.id}">Delete</button>
        `;
        notesList.appendChild(noteItem);
        
        // Add delete event listener
        const deleteBtn = noteItem.querySelector('.delete-btn');
        deleteBtn.addEventListener('click', function() {
            deleteNote(note.id);
        });
    });
}

// Create a new note
function createNote(title, content) {
    fetch('/api/notes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, content }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        
        // Clear the form
        document.getElementById('title').value = '';
        document.getElementById('content').value = '';
        
        // Refresh notes list
        fetchNotes();
    })
    .catch(error => console.error('Error creating note:', error));
}

// Delete a note
function deleteNote(id) {
    fetch(`/api/notes/${id}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        // Refresh notes list
        fetchNotes();
    })
    .catch(error => console.error('Error deleting note:', error));
}