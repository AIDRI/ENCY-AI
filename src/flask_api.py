from flask import Flask, request, json, render_template
import boto3
import torch
from AI.test import prediction
import io

BUCKET_NAME = "ency-ai"
MODEL_FILE_NAME = "distilbert.pt"

app = Flask(__name__)

S3 = boto3.client('s3')


def load_model(key):
	if not os.path.exists('AI\\checkpoints\\distilbert.pt'):
		S3.download_file(BUCKET_NAME, key, 'AI\\checkpoints\\distilbert.pt')


@app.route('/')
def my_form():
	return render_template('my-form.html')


@app.route('/', methods=['GET', 'POST'])
def index():
	doc = request.form['text']
	output = prediction(doc, 10) #length

	out = {"output":output}
	return json.dumps(out)


app.run(host='127.0.0.1')
