from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from database import DB


class Video:

    """
    {
        code: str, level code
        name: str, level name
        programs: List[ObjectId], list of programs

    }
    """

    collection = "videos"
    "5$ for video below 500MB and 12.5$ above 500MB. Additional 12.5$ if the video is under 6 minutes 18 second and 20$ if above. "
    pricing = {"0500":5, "1500":12.5,"0378":12.5, "1378":20 }

    def __init__(
        self,
        filename: str,
        size: int,
        duration: float,

    ):
        self.filename = filename
        self.size = size
        self.duration = duration

    def save(self):
        return DB.insert_one(self.collection, data=self.json())

    def json(self):
        return {
            'filename': self.filename,
            'size': self.size,
            'duration': self.duration,
            'date': datetime.now()
        }

