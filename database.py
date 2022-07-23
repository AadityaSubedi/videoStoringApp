"""
This code provides an abstraction over the pymongo,
mongoDB queries.
It is recommended to call these methods when querying the database
rather than using the pymongo methods.
"""
import os
from typing import Any, Iterable, List, Mapping, Optional, Union

import pymongo
from pymongo.results import (
    DeleteResult,
    InsertManyResult,
    InsertOneResult,
    UpdateResult,
)


class DB:
    # Private variables (DONOT access outside the class)
    _build = os.environ.get("BUILD", "dev")
    _client = pymongo.MongoClient()

    if _build == "dev":
        database = _client.videoapp_dev
    elif _build == "staging":
        database = _client.videoapp_staging
    elif _build == "prod":
        database = _client.videoapp

    # The following methods are used when we expect to work with
    # only one document of a collection.
    # These operate on the first document that matches in the collection.
    # Usually, these methods are recommended to use.
    @staticmethod
    def insert_one(collection: str, data: dict) -> InsertOneResult:
        """
        Insert one document to a collection.

        Args:
            collection (str): The collection to insert to
            data (dict): The data to insert

        Returns:
            InsertOneResult: Returns if succesfull else prints error
        """
        try:
            return DB.database[collection].insert_one(data)
        except pymongo.errors.DuplicateKeyError as dupErr:
            raise Exception(
                f"Duplicated data entry for the {collection} collection "
                f"for {dupErr.details['keyValue']}"
            )

    @staticmethod
    def find_many(
        collection: str,
        query: Mapping[str, Any] = None,
        return_values: Union[Mapping[str, bool], List[str]] = None,
    ) -> pymongo.cursor.Cursor:
        """
        Returns all the documents which match the query
        Args:
            collection (str): Collection Name
            return_values (Union[Mapping[str, bool], List[str]]), optional):
                 The keys to return. Defaults to None.
        Returns:
            pymongo.cursor.Cursor: List like Iterable object
        """
        return DB.database[collection].find(query, return_values)