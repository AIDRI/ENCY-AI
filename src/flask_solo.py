from flask import Flask, request
from AI.test import prediction
from AI.word_extraction import word_extraction
from AI.wiki import search_on_wikipedia
from scrapper.data_scrapper import data_scrapping

app = Flask(__name__)

@app.route('/summary', methods=['GET', 'POST'])
def summary():
	if not request.json:
		return { "error": "No json body found in request" }

	if "text" not in request.json:
		return { "error": "field text not found. Expected string" }

	length = 5
	if "length" in request.json:
		length = request.json['length']

	doc = request.json['text']
	
	output = prediction(doc, length)
	keywords = word_extraction(doc)
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
