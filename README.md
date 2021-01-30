# ENCY-AI

![ENCY_logo](/assets/ency_logo.png)

## Context

This project was realized within the framework of the Timathon #3. The theme of the competition was "Virtual assisstant".  
We had one month to design our Artificial Intelligence, the API, as well as the front-end part of the project.  
The project was realized by Team Coffee.  
The website was made by Milan and Saptarshi, the UI/UX by Karan, the API by Aineas and Adrien.  
Finally, the AI part was made by Adrien (ower of the AI-repo).  

Special thanks to TeckWithTim for hosting the competition.

## Presentation

This is a virtual assistant project that aims to help and simplify a user's web searches.  
The project is aimed at students, bloggers, researchers, and others.  
Team Coffee has therefore imagined a simple API to answer this problem: E.N.C.Y.  
By introducing an article (Wikipedia for example) to the Artificial Intelligence of E.N.C.Y., the BERT algorithm will create a summary of variable size to simplify the readings, but will also suggest interesting or similar readings to the user.

# Installation
Before starting, you must have python 3.7 64 bit installed and running on your system, else some of the
requirements will fail to install.          
1.Run the following commands: virtualenv restapivenv pip install -r requirements.txt            
2.Go to AI/checkpoints/download.sh and run it or open the file and download them manually           
3.Rename the 400 MB file that you just downloaded to bert.pt, the other distilbert.pt          
4.Go to REST_API and run the following command: py manage.py runserver (optional, define the port here)         
Now the server is running and you are ready to make requests to http://domain.com:port/api/text_summarizer/


## Usage

- Lorem Ipsum Dolor

## AI model

The artificial intelligence model used is based on the BERT model.  
This very powerful model using NLP technique is very useful in translation, summarization, and keyword extraction.  
It is especially these last two parts that will be useful to us.  

Since the objective of BERT is to generate a language model, only the coding mechanism is required.  
In its basic form, Transformer has two distinct mechanisms: an encoder that reads the text entered and a decoder that produces a prediction for the task.  
It is therefore considered bi-directional, although it would be more accurate to say that it is non-directional.  
BERT uses the Transformer, an attention mechanism that learns contextual relationships between words (or sub-words) in a text.

## References

1 - [{"BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding", "Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova"}](https://arxiv.org/pdf/1810.04805.pdf)  
2 - [Generating text summaries using GPT-2](https://blog.paperspace.com/generating-text-summaries-gpt-2/) (not used in this first version)
3 - [{"Attention is all you need", "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin"}](https://arxiv.org/abs/1706.03762)
3 - [Huggins Face Github](https://github.com/huggingface/transformers)  
4 - [CNN-DailyMail dataset](https://github.com/JafferWilson/Process-Data-of-CNN-DailyMail)  

## Use our API  

If you use our API in your project, please cite us as :  
{  
&nbsp;&nbsp;title : "ENCY"  
&nbsp;&nbsp;author : "Adrien I"  
&nbsp;&nbsp;date : "1/25/2021"  
&nbsp;&nbsp;adress : "online"  
&nbsp;&nbsp;url : "https://github.com/AIDRI/ENCY-AI/"  
}
