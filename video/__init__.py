from flask import Blueprint
from flask_restful import Api

video_bp = Blueprint("video", __name__, url_prefix="/api")
video_api = Api(video_bp)

from . import routes
