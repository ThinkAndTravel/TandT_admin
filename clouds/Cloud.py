from MongoConnection.MongoConnection import MongoConnector


class Cloud(MongoConnector):
    _id = ""
    key = ""
    secret = ""
    cloudName = ""

    def __init__(self, connection_string, database_name):
        super(Cloud, self).__init__(connection_string, database_name)
        self.get_collection('Cloud')

    def fill(self, __id, _cloudName="", _key="", _secret=""):
        self._id = __id
        self.cloudName = _cloudName
        self.key = _key
        self.secret = _secret

    def make_bson(self):
        return {'_id': self._id, 'Key': self.key,
                                        'Secret': self.secret, 'Cloud_name': self.cloudName}

    def save(self, obj):
        if self.collection.find({'_id': obj._id}).count():
            self.collection.find_one_and_replace({'_id': obj._id}, obj.make_bson())
        else:
            self.collection.insert_one(obj.make_bson())

    def remove(self, obj):
        if self.collection.find({'_id': obj._id}).count():
            self.collection.delete_one({'_id': obj._id})
