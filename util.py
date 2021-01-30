import json
from marshmallow import ValidationError
from bson.objectid import ObjectId
from db import mongo


class MongoEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def mongo_id_decoder(obj):
    # Try to convert str to Mongo Object ID
    try:
        return ObjectId(obj)
    except Exception:
        raise ValidationError("Invalid UserHistory Id Format", "_id")


def validate_userhistory_id(userhistory_id):
    userhistory = mongo.db.userhistory.find_one({"_id": ObjectId(userhistory_id)})
    if not userhistory:
        raise ValidationError("User Id Not Found", "_id")
