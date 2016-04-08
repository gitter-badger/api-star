from coreapi import Document
from api_star.authentication import BasicAuthentication
from api_star.exceptions import NotFound
from api_star.frameworks.falcon import App
from api_star.permissions import IsAuthenticated
from api_star.renderers import CoreJSONRenderer, DocsRenderer
from api_star.schema import add_schema
import uuid


app = App(title='Notes API')


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
def schema():
    """
    Return the API schema.
    """
    return app.schema


@app.get('/notes/')
def list_notes():
    """
    Returns all existing notes.
    """
    return notes


@app.post('/notes/')
def create_note(description, complete=False):
    """
    Creates a new note.

    * description - A short description of the note.
    * [complete] - True if the task has been completed, false otherwise.
    """
    note = {'id': get_id(), 'description': description, 'complete': complete}
    notes.insert(0, note)
    return note


@app.get('/notes/{note_id}/')
def read_note(note_id):
    """
    Reads a single note.

    * note_id - A unique ID string for the note.
    """
    note = lookup(note_id)
    return note


@app.put('/notes/{note_id}/')
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


@app.delete('/notes/{note_id}/')
def delete_note(note_id):
    """
    Deletes a note.

    * note_id - A unique ID string for the note.
    """
    note = lookup(note_id)
    notes.remove(note)
    return ''
