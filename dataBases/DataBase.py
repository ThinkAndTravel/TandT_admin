from MongoConnection.MongoConnection import MongoConnector


class DataBase(MongoConnector):
    _id = ""
    dbName = ""
    connection_string = ""
    dataType = ""

    def __init__(self, connection_string, database_name):
        super(DataBase, self).__init__(connection_string, database_name)
        self.get_collection('DB')

    def fill(self, __id, _dbName="", _connstr="", _dataType=""):
        self._id = __id
        self.dbName = _dbName
        self.connection_string = _connstr
        self.dataType = _dataType

    def make_bson(self):
        return {'_id': self._id, 'ConnectingString': self.connection_string,
                                        'dbName': self.dbName, 'CollectionName': self.dataType}

    def save(self, obj):
        if self.collection.find({'_id': obj._id}).count():
            self.collection.find_one_and_replace({'_id': obj._id}, obj.make_bson())
        else:
            self.collection.insert_one(obj.make_bson())

    def remove(self, obj):
        if self.collection.find({'_id': obj._id}).count():
            self.collection.delete_one({'_id': obj._id})
