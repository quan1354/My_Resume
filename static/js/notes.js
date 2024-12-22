const apiUrl = '/'; // Update with your Django URL prefix if needed
const notesContainer = document.getElementById('notesContainer');
const noteContent = document.getElementById('noteContent');
const noteCategory = document.getElementById('noteCategory');
const saveNoteButton = document.getElementById('saveNoteButton');

const renderNotes = (notes) => {
    notesContainer.innerHTML = '';
    notes.forEach(note => {
        const card = document.createElement('div');
        card.className = 'note-card';
        card.innerHTML = `
            <div class="note-title">${note.category}</div>
            <div class="note-date">${note.date}</div>
            <pre>${note.content}</pre>
            <div class="note-actions">
                <button class="edit" onclick="editNote(${note.id})">Edit</button>
                <button class="delete" onclick="deleteNote(${note.id})">Delete</button>
            </div>
        `;
        notesContainer.appendChild(card);
    });
};

const fetchNotes = async () => {
    const response = await fetch(`${apiUrl}get_notes/`);
    const notes = await response.json();
    renderNotes(notes);
};

saveNoteButton.addEventListener('click', async () => {
    const content = noteContent.value.trim();
    const category = noteCategory.value;
    if (!content || !category) return alert('Please fill out all fields.');
    console.log('hhh')
    await fetch(`${apiUrl}save_note/`, {
        method: 'POST',
        body: JSON.stringify({ content, category, date: new Date().toLocaleString(), id: Date.now() }),
    });
    noteContent.value = '';
    fetchNotes();
});

window.deleteNote = async (id) => {
    await fetch(`${apiUrl}delete_note/`, {
        method: 'POST',
        body: JSON.stringify({ id }),
    });
    fetchNotes();
};

window.editNote = async (id) => {
    const notes = await fetch(`${apiUrl}get_notes/`).then(res => res.json());
    const noteToEdit = notes.find(note => note.id === id);
    if (!noteToEdit) return;
    noteContent.value = noteToEdit.content;
    noteCategory.value = noteToEdit.category;
    await fetch(`${apiUrl}delete_note/`, {
        method: 'POST',
        body: JSON.stringify({ id }),
    });
    fetchNotes();
};

fetchNotes();
