from app import app
from flask import request
# import boto3
from AI.test import prediction
from AI.word_extraction import word_extraction
from AI.wiki import search_on_wikipedia
from scrapper.data_scrapper import data_scrapping
from va.chatter import chatter
from os import getenv

from dotenv import load_dotenv

load_dotenv()

api_key = getenv('API_SECRET_KEY', None)
assert api_key


"""
BUCKET_NAME = "ency-ai"
MODEL_FILE_NAME = "distilbert.pt"
"""


@app.route('/chatter', methods=['GET', 'POST'])
def chatterReq():
	if not request.json:
		return { "error": "No json body found in request" }

	if "text" not in request.json:
		return { "error": "field text not found. Expected string" }

	if request.headers.get('X-API-KEY') != api_key:
		return { "error" : "Invalid API Key included." }	

	doc = request.json['text']
	
	output = chatter(doc)
	out = {
			"output": output
		  }
	return out


@app.route('/summary', methods=['GET', 'POST'])
def summary():
	if not request.json:
		return { "error": "No json body found in request" }

	if "text" not in request.json:
		return { "error": "field text not found. Expected string" }

	if request.headers.get('X-API-KEY') != api_key:
		return { "error" : "Invalid API Key included." }	

	length = 5
	if "length" in request.json:
		length = request.json['length']

	doc = request.json['text']
	
	output = prediction(doc, length)
	keywords = word_extraction(str(output))
	recommended_articles = search_on_wikipedia(keywords)

	out = {
			"output": output, 
			"keywords": keywords,
			"recommended_articles": recommended_articles
		  }
	return out


@app.route('/summarise-url')
def summarise_url():
	if not request.json:
		return { "error": "No json body found in request" }
	
	if "url" not in request.json:
		return { "error": "field url not found. Expected string" }

	url = request.json["url"]

	length = 5
	if "length" in request.json:
		length = request.json['length']

	scrapped_data = data_scrapping(url)
	if "error" in scrapped_data:
		return {"error": "Website does not allow scrapping"}

	if request.headers.get('X-API-KEY') != api_key:
		return { "error" : "Invalid API Key included." }	

	output = prediction(scrapped_data["output"], length) #length
	keywords = word_extraction(str(output))
	recommended_articles = search_on_wikipedia(keywords)

	out = {
			"output": output, 
			"keywords": keywords,
			"recommended_articles": recommended_articles
		  }
	return out

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True, port=80)
