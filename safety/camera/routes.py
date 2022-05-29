from flask import render_template
from flask import Blueprint

camera = Blueprint('camera', __name__)

@camera.route("/videos")
def video_play():
    return render_template('videos.html')

