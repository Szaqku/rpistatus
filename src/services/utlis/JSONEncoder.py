import json
from bson import ObjectId, json_util


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

    def decode_to_dict(self, data: any):  # TODO: Fix this function, it's so fkin unoptimized but works for now
        return json_util.loads(self.encode(data))
