
from email import message
from os import error
import re
from flask import Flask, app, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break
        
    return code

@app.route('/', methods=['GET', 'POST'])
def home():
    session.clear()
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        join = request.form.get('join', False)
        create = request.form.get('create', False)

        if not name:
            return render_template("home.html", error="please enter a name.", name=name, code=code)
        
        if join != False and not code:
            return render_template("home.html", error="please enter a room code.", name=name, code=code)
        
        room = code

        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}

        elif code not in rooms:
            return render_template('home.html', error="Room does not exist.", name=name, code=code)
        
        session['name'] = name
        session['room'] = room
        return redirect(url_for('room'))

    return render_template("home.html")


#asd
if __name__ == "__main__":
    socketio.run(app, debug=True)