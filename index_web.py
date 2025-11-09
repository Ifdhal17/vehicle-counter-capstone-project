import cv2
from flask import Flask, render_template, Response
from flask_socketio import SocketIO
from trackerr import Tracker
from ultralytics import YOLO
from utill import draw_counter, draw_label, update_counter, trigger_line

CONFIDENCE_THRESHOLD = 0.8
GREEN = (0, 255, 0)
RED = (0, 0, 255)

# Flask app and SocketIO setup
app = Flask(__name__)
socketio = SocketIO(app)

# Initialize video capture and YOLO model
video = cv2.VideoCapture("Untitled.mp4")
model = YOLO("/Users/khansafca/Documents/bangkit/vehicle-counter-capstone-project/yolov8s-300epoch.pt")
model.fuse()

counter = {"car": 0, "truck": 0, "motorbike": 0, "bus": 0}
tracker = Tracker()

line_point1 = (125, 480)
line_point2 = (738, 705)
offset = 12

# {0: 'bus', 1: 'car', 2: 'motorbike', 3: 'truck'}
classes_dict = model.model.names  # type: ignore


from datetime import datetime

# Store historical data for graph
graph_data = {"timestamps": [], "car": [], "truck": [], "motorbike": [], "bus": []}


def update_graph_data(counter):
    """Update graph data with the latest counter values and timestamps."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    graph_data["timestamps"].append(timestamp)
    graph_data["car"].append(counter["car"])
    graph_data["truck"].append(counter["truck"])
    graph_data["motorbike"].append(counter["motorbike"])
    graph_data["bus"].append(counter["bus"])

    # Limit the data to the last 50 entries for performance
    if len(graph_data["timestamps"]) > 50:
        for key in graph_data.keys():
            graph_data[key].pop(0)

    # Emit the updated graph data
    socketio.emit('update_graph', graph_data)


def generate_frames():
    """Generator function to stream video frames."""
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        cv2.line(frame, line_point1, line_point2, color=RED, thickness=3)

        results = model.predict(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
        if results[0].boxes is not None:
            bounding_box = results[0].boxes.xyxy.tolist()
            classes_idx = results[0].boxes.cls.tolist()
            confidence_score = results[0].boxes.conf
            tracked_bounding_box = tracker.update(bounding_box)

            for bbox, cls, conf in zip(tracked_bounding_box, classes_idx, confidence_score):
                x1, y1, x2, y2, object_id = [int(value) for value in bbox]
                cv2.rectangle(frame, (x1, y1), (x2, y2), color=GREEN, thickness=1)
                draw_label(frame, classes_dict, cls, x1, y1, object_id)

                if trigger_line(line_point1[1], line_point2[1], offset, [y1, y2]):
                    update_counter(cls, counter)

            draw_counter(frame, counter)

        # Emit counter and graph data
        socketio.emit('update_counter', counter)
        update_graph_data(counter)

        # Encode frame as JPEG and yield it
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break




@app.route('/')
def index():
    """Home route that renders the HTML page."""
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection."""
    socketio.emit('update_counter', counter)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5003)
