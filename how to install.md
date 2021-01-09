# REST API + ENCY AI

# Before starting, you must have python 3.7 64 bit installed and running on your system, else some of the
# requirements will fail to install.

1. Run the following commands: virtualenv restapivenv    pip install -r requirements.txt
2. Go to AI/checkpoints/download.sh and run it or open the file and download them manually
3. Rename the 400 MB file that you just downloaded to bert.pt, the other distilbert.pt
4. Go to REST_API and run the following command: py manage.py runserver (optional, define the port here)
5. Now the server is running and you are ready to make requests to http://domain.com:port/api/text_summarizer/