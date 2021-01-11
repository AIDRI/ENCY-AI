from flask import Flask, request, json, render_template
import boto3
import torch
from AI.test import prediction
from AI.models.word_extraction import word_extraction
from AI.wiki import search_on_wikipedia
import io

BUCKET_NAME = "ency-ai"
MODEL_FILE_NAME = "distilbert.pt"

app = Flask(__name__)

S3 = boto3.client('s3')


def load_model(key):
	pass
	#S3.download_file(BUCKET_NAME, key, 'AI\\checkpoints\\distilbert.pt')


@app.route('/')
def my_form():
	return render_template('my-form.html')


@app.route('/', methods=['GET', 'POST'])
def index():
	model = load_model(MODEL_FILE_NAME)

	doc = request.form['text']
	output = prediction(doc, 2)
	#words = word_extraction(output[0])
	#article = search_on_wikipedia(words)

	out = {"output":output}
	return json.dumps(out)


app.run(host='127.0.0.1')
