from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

def main():

	users = [{
		"_id" : "he",		#username
		"name": "HE",		#name
		"password": "123",	#password
		"couple": True		#couple
		},
		{
		"_id" : "she",
		"name": "SHE",
		"password": "456",
		"couple": True
		},
		{
		"_id" : "friend1",
		"name": "FRIEND 1",
		"password": "789",
		"couple": False
		}
	]
	db = MongoClient()["imagegallery"]

	collection = db["users"]

	for user in users:
		user['password'] = generate_password_hash(user['password'], method='pbkdf2:sha256')
		try:
			collection.insert(user)
			print("User created")
		except DuplicateKeyError:
			print("User already exists")

	
	collist = db.list_collection_names()
	db['photos'].drop()
	if "photos" in collist:
		print("Collection already exists")
	else:
		print("Collection created")
		collection = db['photos']


if __name__ == '__main__':
    main()