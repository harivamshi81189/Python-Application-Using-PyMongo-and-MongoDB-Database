import pymongo as pm
import datetime

fh = open("vocabulary_set.csv",'r')
wd_list= fh.readlines()

wd_list.pop(0)

vocab_list = []
for rawstring in wd_list:
    word, definition = rawstring.split(',',1)
    definition = definition.rstrip()
    vocab_list.append({'word':word,'definition':definition})

client = pm.MongoClient("mongodb://localhost:27017/")
db = client["vocab"]


vocab_col = db["vocab_list"]
vocab_col.drop()
vocab_dict = {'word':'cryptic','definition':'secret with hidden meaning'}
res=vocab_col.insert_one(vocab_dict)
print("inserted_id:",res.inserted_id)
dbs = client.list_database_names()
if "vocab" in dbs:
    print("Database exists")
res = vocab_col.insert_many(vocab_list)
# print(res.inserted_ids)
data = vocab_col.find_one()
print(data)

for data in vocab_col.find({}, {"_id":0,"definition":0}):
    print(data)
data = vocab_col.find_one({'word':'boisterous'})
print(data)
upd = vocab_col.update_one({'word':'boisterous'}, {'$set':{"definition":"rowdy; noisy"}})
print("modified count: ",upd.modified_count)
data = vocab_col.find_one({'word':'boisterous'})
print(data)
upd = vocab_col.update_many({}, {"$set":{"last_updated UTC:":datetime.datetime.utcnow().strftime('%Y-%m-%d%H%M%SZ')}})
print("modified count: ",upd.modified_count)