from time import sleep
from bson.objectid import ObjectId
from flask_restful import Resource
from json import loads

from . import video_api
from flask import Flask, request
from datetime import datetime

from bson.json_util import dumps
from . import helper_functions as vhf
from .models import Video


from database import DB
import ffmpeg
from io import BytesIO
import os
from flask import current_app as app
import cv2
from PIL import Image
import tempfile

from dateutil import parser


@video_api.resource("/upload")
class Videos(Resource):
    def post(self):
        try:
            file = request.files['video']
            filename, size, durations = vhf.save_video(file)
            _id = Video(filename, size, durations).save().inserted_id
            print(size, durations)
            return (vhf.success(
                    "video upload",
                    "video uploaded succesfully",
                    {"filename": filename,
                     "_id": loads(dumps(_id))}
                    ),
                    200
                    )

        except Exception as e:
            return (vhf.failure(

                    "video upload",
                    str(e),
                    ),
                    500
                    )

    def get(self):
        try:
            videos = DB.find_many(Video.collection, {})
            # print(loads(dumps(videos)))
            return (vhf.success(
                    "video upload",
                    "video uploaded succesfully",
                    loads(dumps(videos))
                    ),
                    200
                    )

        except Exception as e:
            return (vhf.failure(

                    "video upload",
                    str(e),
                    ),
                    500
                    )


@video_api.resource("/charge")
class OneVideo(Resource):
    def get(self):
        try:

            data = request.get_json()
            """ data:dict = {"size":float(in MB) , "length(in sec)": float , "type": str}"""
            assert int(data["size"]) <= 1*1024, f"video limit is 1GB"
            assert int(data["length"]) <= 600, f"video limit is 10 min"

            price = Video.pricing[f"{+(data['size']>500)}500"] + \
                Video.pricing[f"{+(data['length']>6*60+18)}378"]

            # return the command line output as the response
            return (vhf.success(
                    "price calculation",
                    "price calculated succesfully",
                    {"price": price}
                    ),
                    200
                    )

        except Exception as e:
            return (vhf.failure(

                    "price calculation",
                    str(e),
                    ),
                    500
                    )


@video_api.resource("/filter")
class FilteredVideo(Resource):
    def get(self):
        try:

            data = request.get_json()
            """ data:dict = {"minDate":ISODate(), "maxDate": ISODate(), minSize: int, maxSize: int }"""
            # min_date = data["minDate"]
            min_size = data.get("minSize")
            max_size = data.get("maxSize")
            min_date = data.get("minDate") and parser.parse(data.get("minDate"))
            max_date = data.get("maxDate") and parser.parse(data.get("maxDate"))

            videos = DB.find_many(Video.collection, {"$or": [
                {
                    "size": {
                        "$gte": min_size,
                        "$lte": max_size
                    }
                },
                {
                    "date": {
                        "$gte": min_date,
                        "$lte": max_date
                    }
                }
            ]})

            # return the command line output as the response
            return (vhf.success(
                    "price calculation",
                    "price calculated succesfully",
                    loads(dumps(videos))
                    ),
                    200
                    )

        except Exception as e:
            return (vhf.failure(

                    "price calculation",
                    str(e),
                    ),
                    500
                    )
