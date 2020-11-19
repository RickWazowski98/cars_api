import pymongo


class Db():
    def __init__(self):
        self.collection = self.connect_to_db()

    def connect_to_db(self):
        client = pymongo.MongoClient('localhost', 27017)
        db = client['API']
        collection = db['Cars']
        collection.create_index("VIM", unique=True)
        return collection

    def insert_document(self, data):
        self.collection.insert_one(data)

    def update_document(self, query_elements, new_value):
        self.collection.update_one(query_elements, {'$set': new_value})

    def show_documents(self):
        result = self.collection.find({}, {"_id": 0})
        return [r for r in result]
