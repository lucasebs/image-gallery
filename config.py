import os
from pymongo import MongoClient


WTF_CSRF_ENABLED = True
SECRET_KEY = os.urandom(32)

DB_NAME = 'imagegallery'

DATABASE = MongoClient()[DB_NAME]

PHOTOS_COLLECTION = DATABASE.photos
USERS_COLLECTION = DATABASE.users

DEBUG = True

IMAGE_UPLOAD_PATH = "./uploads"
ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF"]
MAX_IMAGE_FILESIZE = 0.5 * 1024 * 1024


S3_BUCKET="image-gallery-pending"
S3_KEY="AKIAVKPDV4CBOB4UQMON"
S3_SECRET_ACCESS_KEY="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"
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
