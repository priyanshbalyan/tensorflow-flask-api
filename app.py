from flask import Flask, render_template, request, jsonify
import classify_image as cfi
from flask_socketio import SocketIO
import os

def render_file(filename):
	f = open(filename, 'r')
	return f.read()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def static_page():
	return render_file('index.html')

@app.route('/b')
def b():
	return os.path.join(os.path.dirname(__file__), 'tmp.jpg')

@socketio.on('my event')
def handle_my_custom_event(json):
	print('received json : ' + str(json))

@app.route('/upload', methods =['GET', 'POST'])
def handle_file():
	if request.method == 'POST':
			f = request.files['file']
			f.save('tmp.jpg')
			answer = cfi.run_inference_on_image()
			print(os.path.join(os.path.dirname(__file__),'tmp.jpg'))
	return jsonify(status="OK", results=answer)

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)