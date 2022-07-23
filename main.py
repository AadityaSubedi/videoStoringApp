from flask import Flask, Blueprint, send_from_directory, render_template

from flask_jwt_extended import JWTManager
from video import video_bp
from flask_restful import Resource, Api
from flask_cors import CORS
import os



UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)




app.register_blueprint(video_bp)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JWT_SECRET_KEY'] = 'will_edit_this_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 *1024 #1GB 
app.config['ALLOWED_EXTENSIONS'] = ['mp4', 'mkv']





@app.route("/")
def hello():
    return {1:"testing"}

@app.route('/videos/<string:videoname>')
def download_video(videoname):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               'videos/'+videoname)


jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    return {
        'data1': 'happy coding ',
        'data2': 'happy coding 2'
    }


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(decrypted_token):
    return decrypted_token['jti'] in {"blocklist"}
    #  modify this as per the need later


CORS(app)  # This will enable CORS for all routes


if __name__ == "__main__":
    app.run()

