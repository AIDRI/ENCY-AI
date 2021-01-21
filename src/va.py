#from app import app
from flask import Flask, request
# import boto3
from va.chatter import chatter

app = Flask(__name__)

@app.route('/chatter', methods=['GET', 'POST'])
def chat_bot():
	if not request.json:
		return { "error": "No json body found in request" }

	if "text" not in request.json:
		return { "error": "field text not found. Expected string" }

	doc = request.json['text']
	
	output = chatter(doc)
	out = {
			"output": output
		  }
	return out


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True, port=80)
