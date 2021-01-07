# Research-assistant

1- Clone the repo  
2- Go to ENCY/  
3- pip install -r requirements.txt  
4- Go to checkpoints/  
5- Run download.sh (or edit it and download each checkpoint, make sure to rename the checkpoint)  
6- Go to test/input.txt  
7- Add your article (it s better if the article haven't some characters bug, or image description, etc...)  
8- Return to ENCY/  
9- Go to test.py  
10- Change the var mode, two types of model : distilbert (fast), bert (slow)  
11- In predict, change the last number (here 10) by the length of summary  
12- Go to cmd and do py test.py

The result is in test/out.txt
