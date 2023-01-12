from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import json
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

roomUser = "support"


#chatbot init 
chatbot = ChatBot("sam", logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'threshold': 0.55,
            'default_response': 'default_value'
        }
    ],)
ListTrainer(chatbot)

connectedUsers = []

@app.route('/')
def index():
    return render_template('chat-bot-with-support.html')


@app.route('/admin')
def admin():
    return render_template('admin-chat.html')

@app.route('/get-resp')
def getResponse():
    q = request.args.get('query')
    frm = request.args.get('sid')
    print(q)
    print(frm)
    resp = chatbot.get_response(q)
    if(resp.text == "default_value"):
        socketio.emit('message', {'msg': q, 'from' : frm}, room=roomUser)
        return "def-001"
    else:
        return resp.text


@socketio.on('connect')
def conectEvent():
    join_room(roomUser)
    print("Connected")

@socketio.on('text')
def messagingEvent(message):
    if message['from'] == None:
        message['from'] = request.sid
    print(message)
    emit('message', {'msg': message['msg'], 'from' : message['from']}, room=roomUser)