
from cgi import FieldStorage
from database import DB
from werkzeug.datastructures import FileStorage
from typing import TextIO
from flask import current_app as app    
import ffmpeg
import os
import uuid
import tempfile
from typing import AbstractSet, Any, Iterable, Mapping, Optional, Set, Union
JSONType = Mapping[str, Any]

def save_video(file: FileStorage) -> str:
    """
    Checks if the file is valid and saves it.
    Args:
        file (FileStorage): A file uploaded to flask obtained from request.files
    Returns:
        str: The filename of the saved file if its valid else assertion error is thrown
    """

    assert file.filename, "No video selected."
    extension = is_video(file.filename)
    durations = None
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(file.stream.read())
        durations =  is_valid_duration(fp)
        size = os.path.getsize(fp.name)
        file.seek(0,0)

    directory = os.path.join(os.getcwd(), app.config["UPLOAD_FOLDER"], "videos")

    # !Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    filename = f"{uuid.uuid4()}.{extension}"
    file.save(os.path.join(directory, filename))

    # file size, 
    return filename,size, durations


def is_valid_duration(fp: TextIO)-> float:
    # validate file duration, 
    details = ffmpeg.probe(fp.name)["streams"]
    durations = details[0]["duration"]
    assert float(durations) <= 600 ,f"video exceeded limit of 10 min"
    return durations

    # valid duration is : 10 min




def is_video(filename:str) -> str:
    extension  = '.' in filename  and filename.rsplit('.', 1)[1].lower()
    print(extension)
    assert extension in app.config["ALLOWED_EXTENSIONS"], f"invalid video extension .{extension}"
    return extension
    


def success(operation: str, msg: str, data: Optional[JSONType] = None) -> JSONType:
    """
    This function returns a formatted dictionary for the successful cases.
    Args:
        operation (str): Operation successfully completed
        msg (str): Sucessful Message
        data (Optional[JSONType], optional): Data to be sent. Defaults to None.
    Returns:
        JSONType: Formatted Dictionary
    """
    return {
        "operation": operation,
        "success": True,
        "message": msg,
        "data": data,
    }


def failure(operation: str, msg: str) -> Mapping[str, Union[str, bool]]:
    """
    This function returns a formatted dictionary for the failure cases, or exceptions.
    Args:
        operation (str): Operation that failed
        msg (str): Failure Message
    Returns:
        Mapping[str, Union[str, bool]]: Formatted Dictionary
    """
    return {
        "operation": operation,
        "success": False,
        "message": msg,
    }

