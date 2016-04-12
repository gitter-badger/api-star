from coreapi import Document
from api_star import validators
from api_star.decorators import validate
from api_star.exceptions import NotFound
from api_star.frameworks.flask import App
from api_star.renderers import CoreJSONRenderer, DocsRenderer
import uuid


app = App(__name__, title='Notes API')


def lookup(note_id):
    for note in notes:
        if note['id'] == note_id:
            return note
    raise NotFound()


def get_id():
    return '%s' % uuid.uuid4()


notes = [
    {'id': get_id(), 'description': 'Meet someone', 'complete': True},
    {'id': get_id(), 'description': 'Walk somewhere', 'complete': False},
    {'id': get_id(), 'description': 'Do something', 'complete': False},
]


@app.get('/', renderers=[CoreJSONRenderer(), DocsRenderer()], exclude_from_schema=True)
def root():
    """
    Return the API details, either as documentation, or as a schema representation.
    """
    return app.schema


@app.get('/notes/')
def list_notes():
    """
    Returns all existing notes.
    """
    return notes


@app.post('/notes/')
@validate(description=validators.text(max_length=100))
def create_note(description):
    """
    Creates a new note.

    * description - A short description of the note.
    """
    note = {'id': get_id(), 'description': description, 'complete': False}
    notes.insert(0, note)
    return note


@app.get('/notes/<note_id>/')
def read_note(note_id):
    """
    Reads a single note.

    * note_id - A unique ID string for the note.
    """
    note = lookup(note_id)
    return note


@app.put('/notes/<note_id>/')
@validate(
    description=validators.text(max_length=100),
    complete=validators.boolean()
)
def update_note(note_id, description=None, complete=None):
    """
    Update a note.

    * note_id - A unique ID string for the note.
    * [description] - A short description of the note.
    * [complete] - True if the task has been completed, false otherwise.
    """
    note = lookup(note_id)
    if description is not None:
        note['description'] = description
    if complete is not None:
        note['complete'] = complete

    return note


@app.delete('/notes/<note_id>/')
def delete_note(note_id):
    """
    Deletes a note.

    * note_id - A unique ID string for the note.
    """
    note = lookup(note_id)
    notes.remove(note)
    return ''
