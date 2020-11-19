import pymongo
# datas = {"manufacturer":"HAMMER","model":"NONE","year_of_issue":"2010","colour":"Grey","VIM":"0004"}

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

    def find_document(self, elements, multiple=False):
        if multiple:
            result = self.collection.find(elements)
            return [r for r in result]
        else:
            return self.collection.find_one(elements)

    def show_documents(self):
        result = self.collection.find({},{"_id":0})
        return [r for r in result]

# Db().insert_document(datas)