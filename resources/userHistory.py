from flask import json
from flask_restful import Resource
from marshmallow import Schema, fields
from webargs.flaskparser import use_args
from db import mongo
from util import mongo_id_decoder, validate_userhistory_id

class GetHistorySchema(Schema):
    location = fields.Str()
    rating = fields.Int()

class PostHistorySchema(Schema):
    location = fields.Str(required=True)
    rating = fields.Int(required=True)

class GetSchema(Schema):
    _id = fields.Function(deserialize=mongo_id_decoder)
    History = fields.List(fields.Nested(GetHistorySchema()))


class PostSchema(Schema):
    History = fields.List(fields.Nested(PostHistorySchema()))


class PutQuerySchema(Schema):
    _id = fields.Function(
        deserialize=mongo_id_decoder, validate=validate_userhistory_id, required=True
    )

class PutBodySchema(Schema):
    History = fields.List(fields.Nested(PostHistorySchema()))


class DeleteSchema(Schema):
    _id = fields.Function(
        deserialize=mongo_id_decoder, validate=validate_userhistory_id, required=True
    )

class UserHistory(Resource):
    @use_args(GetSchema(), location="querystring")
    def get(self, query):
        # Search for all users that match query arguments
        userhistories = [userhistory for userhistory in mongo.db.userhistory.find(query)]
        return json.jsonify(data=userhistories)

    @use_args(PostSchema(), location="json")
    def post(self, body):
        # Create user with data from request
        mongo.db.userhistory.insert_one(body)
        return json.jsonify(data=body)

    @use_args(PutQuerySchema(), location="querystring")
    @use_args(PutBodySchema(), location="json")
    def put(self, query, body):
        userhistory_id = query.get("_id")
        # Update user with data from request
        mongo.db.userhistory.update_one({"_id": userhistory_id}, {"$set": body})
        updated_userhistory = mongo.db.userhistory.find_one({"_id": userhistory_id})
        return json.jsonify(data=updated_userhistory)

    @use_args(DeleteSchema(), location="querystring")
    def delete(self, query):
        user_id = query.get("_id")
        # Delete user based on _id
        mongo.db.userhistory.delete_one({"_id": user_id})
        return {"message": "UserHistory was deleted"}