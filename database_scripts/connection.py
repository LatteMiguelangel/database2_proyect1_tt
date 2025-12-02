from pymongo import MongoClient

uri = "mongodb+srv://migueleonet571_db_user:6i1ElWW08zwNOGWX@cluster0.vispj9i.mongodb.net/?appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri)
db = client["proyect1database2"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)