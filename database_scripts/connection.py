from pymongo import MongoClient

# Usamos la URI que ya confirmaste que funciona
uri = "mongodb+srv://migueleonet571_db_user:6i1ElWW08zwNOGWX@cluster0.vispj9i.mongodb.net/?appName=Cluster0"

# Crear cliente y conectar
client = MongoClient(uri)
db = client["proyect1database2"]

# Probar conexión
try:
    client.admin.command("ping")
    print("Conexión exitosa a MongoDB Atlas")
    print("Bases de datos disponibles:", client.list_database_names())
except Exception as e:
    print("Error de conexión:", e)