# How to install the REST API ?

### Before starting, make sure you have Python 3.7 64 bits installed on your computer. Make sure that you are using the 3.7 64 bits version. To be sure, go to "cmd" and write python.

## Installation

1. Run the following command to create a virtual env : virtualenv restapivenv  (make sure to activate the env)
2. Run the following command to install the requirements : pip install -r requirements.txt  
3. Go to AI/checkpoints/download.sh and run it to install pre-trained weights, or download the model at : https://www.googleapis.com/drive/v3/files/1WxU7cHECfYaU32oTM0JByTRGS5f6SYEF?alt=media&key=AIzaSyCmo6sAQ37OK8DK4wnT94PoLx5lx-7VTDE . Make sure to rename it (distilbert.pt, and move it to checkpoints)  
4. Go to REST_API and run the following command: py manage.py runserver (optional, define the port here)
5. Now the server is running and you are ready to make requests to http://domain.com:port/api/text_summarizer/

## Usage

To use the AI, after opening the localhost, you will have three fields to complet :
1. Add a text to summarize
2. Choose the length of the summary
3. Choose "yes" if you want to have keywords extraction, and websites suggestions (wikipedia)