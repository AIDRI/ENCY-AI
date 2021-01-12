from flask import request
# import boto3
from AI.test import prediction

BUCKET_NAME = "ency-ai"
MODEL_FILE_NAME = "distilbert.pt"

from app import app

# S3 = boto3.client('s3')


# def load_model(key):
# 	pass
	#S3.download_file(BUCKET_NAME, key, 'AI\\checkpoints\\distilbert.pt')


@app.route('/')
def index():
	if not request.json:
		return { "error": "No json body found in request" }

	if "text" not in request.json:
		return { "error": "No text field in json body" }

	print("TEST")
	doc = request.json['text']

	output = prediction(doc, 5) #length

	out = {"output":output}
	return out

@app.route('/test')
def test():
	return { "out": "works" }

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True, port=80)
