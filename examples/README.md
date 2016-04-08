Running `examples/todo_flask.py`:

    pip install flask flask-cli
    flask --app examples.todo_flask --debug run

Running `examples/todo_falcon.py`:

    pip install falcon gunicorn
    gunicorn examples.todo_falcon:app
