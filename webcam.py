from threading import Thread, Lock
from flask import Flask, abort, Response, make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import cv2
import time
from datetime import datetime

camera = cv2.VideoCapture(0)
latest_image = None
mutex = Lock()

app = Flask(__name__)
auth = HTTPBasicAuth()

USERS = {
    'XXX': generate_password_hash('YYY')
}

@auth.verify_password
def verify_password(username: str, password: str) -> str:
    global USERS
    if username in USERS and \
            check_password_hash(USERS.get(username), password):
        return username

def capture_images() -> None:
    global latest_image, camera, mutex
    time.sleep(1)
    while True:
        _, image = camera.read()
        image = cv2.resize(image, [640, 480], cv2.INTER_CUBIC)
        timestamp = datetime.utcnow()
        image = cv2.putText(
            image, timestamp.strftime("%Y-%m-%d %H:%M:%S"), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
            (0, 255, 0), 2, cv2.LINE_AA)
        _, image = cv2.imencode('.jpeg', image)
        mutex.acquire()
        try:
            latest_image = image
        finally:
            mutex.release()
            time.sleep(1)

@app.route('/')
@auth.login_required
def get_latest_image() -> Response:
    global latest_image, mutex
    mutex.acquire()
    try:
        if latest_image is None:
            return abort(404)

        response = make_response(latest_image.tobytes())
        response.headers['Content-Type'] = 'image/jpeg'
        return response
    finally:
        mutex.release()

if __name__ == '__main__':
    try:
        camera_thread = Thread(target = capture_images)
        camera_thread.start()
        app.run(host='0.0.0.0', port=8081)
    finally:
        camera.release()
        del(camera)
