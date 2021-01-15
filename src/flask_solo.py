from flask import Flask, request
from AI.test import prediction

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
	
	output = prediction(doc, length) #length

	out = {"output":output}
	return out


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True, port=80)
