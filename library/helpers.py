import boto3

def _allowed_image(app, filename):

	if not "." in filename:
		return False

	ext = filename.rsplit(".", 1)[1]

	if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
		return True
	else:
		return False


def _allowed_image_filesize(app, filesize):

	if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
		return True
	else:
		return False


def _get_s3_resource(app):
	if app.config['S3_KEY'] and app.config['S3_SECRET_ACCESS_KEY']:
		return boto3.resource(
			"s3",
			aws_access_key_id=app.config['S3_KEY'],
			aws_secret_access_key=app.config['S3_SECRET_ACCESS_KEY']
		)
	else:
		return boto3.resource("s3")

# def _get_s3_client():
# 	if app.config['S3_KEY'] and app.config['S3_SECRET_ACCESS_KEY']:
# 		return boto3.client('s3',
# 							aws_access_key_id=app.config['S3_KEY'],
# 							aws_secret_access_key=app.config['S3_SECRET_ACCESS_KEY'])
# 	else:
# 		return boto3.client("s3")

def get_bucket(app):
	s3_resource = _get_s3_resource(app)
	return s3_resource.Bucket(app.config["S3_BUCKET"])

def get_s3_url(app, filename):
	return app.config['S3_LOCATION']+filename

def _get_sort(app, sort):
	s = {
		"newest-to-older":{
			"field":"date",
			"order":-1,
			"description": "Newest to Older"
		},	
		"older-to-newest":{
			"field":"date",
			"order":1,
			"description": "Older to Newst"
		},	
		"likes-asc":{
			"field":"likes",
			"order":1,
			"description": "Likes Asc."
		},	
		"likes-desc":{
			"field":"likes",
			"order":-1,
			"description": "Likes Desc."
		},	
	}
	return s[sort]

# def _set_sort(sort):
# 	_sort = sort