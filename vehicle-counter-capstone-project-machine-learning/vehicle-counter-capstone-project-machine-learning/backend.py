from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO
import os

# Create Flask app
app = Flask(__name__)

# Configure SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

# Serve index.html
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# SocketIO event listener for "counter"
@socketio.on('counter')
def handle_counter(data):
    print(f"Received counter message: {data}")


@socketio.on("connect")
def prinout():
    print("Someone connected!")


# Run the server
if __name__ == '__main__':
    # Ensure the static folder exists
    if not os.path.exists("static"):
        os.makedirs("static")

    # Ensure the js folder exists
    js_folder = os.path.join("static", "js")
    if not os.path.exists(js_folder):
        os.makedirs(js_folder)

    # Run Flask with SocketIO
    socketio.run(app, host='0.0.0.0', port=8000)
